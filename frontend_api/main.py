from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from os import getenv
import requests
from typing import Optional, Dict
from openai import OpenAI
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
)

# Retrieve environment variables
DB_API = getenv("DB_API")
OPEN_AI_KEY = getenv('OPEN_AI_KEY')

# Validate environment variables
if not DB_API:
    logger.error("DB_API environment variable not set.")
    raise ValueError("DB_API environment variable not set.")

if not OPEN_AI_KEY:
    logger.error("OPEN_AI_KEY environment variable not set.")
    raise ValueError("OPEN_AI_KEY environment variable not set.")

# API endpoint for properties collection
props_collection = f"{DB_API}/properties"

# Define the request model
class SearchRequest(BaseModel):
    query: str
    params: Optional[Dict] = None  # Optional for future use

def prompt_to_params(msg: str) -> Dict:
    client = OpenAI(
        api_key=OPEN_AI_KEY
    )
    
    instructions = """
    You are a realtor. From the given text, recognize the building parameters mentioned. For example:
    "nákup bytu 4+kk Praha 4 65m2 do 6 mil korun, s balkonem a sklepem."

    You should return a JSON object with the following structure:
    {
        "transaction": "buy",
        "property_type": "flat",
        "size_kk": "4+kk",
        "city": "Praha-5",
        "size_m2": 65,
        "price": 6000000,
        "currency": "czk",
        "balcony": true,
        "cellar": true
    }

    Only include "balcony" and "cellar" if they are mentioned in the text. Ensure all other fields are present as per the structure.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": msg},
            ],
            temperature=0  # Set to 0 for deterministic output
        )
    except Exception as e:
        logger.error(f"OpenAI API request failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the query with OpenAI.")

    # Extract the text response from OpenAI
    params_text = response.choices[0].message.content.strip()
    logger.info(f"OpenAI response text: {params_text}")

    # Convert the text to a dictionary
    try:
        params = json.loads(params_text)
        logger.info(f"Parsed parameters: {params}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters generated from the query.")

    return params

def get_properties_by_params(params: Dict) -> Dict:
    url = f'{DB_API}/{params["transaction"]}'  # Dynamically use 'rents' or 'buys' collection

    # Remove 'transaction' from params before sending to the database API
    params.pop("transaction", None)

    try:
        # Use the correct syntax for passing `params` to the GET request
        response = requests.get(url=url, params=params)
        response.raise_for_status()  # Raise an exception for bad HTTP status codes
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get properties: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve properties.")

@app.post("/api/search")
async def search_properties(search_request: SearchRequest):
    logger.info(f"Received search request with query: {search_request.query}")

    # Use the 'params' if provided; otherwise, generate them
    if search_request.params:
        params = search_request.params
    else:
        params = prompt_to_params(search_request.query)
        params['index'] = 0
        # index sets that we want to load 1st page

    # Fetch properties from db-api with the constructed parameters
    properties = get_properties_by_params(params)

    # Prepare response
    res = {
        "original_query": search_request.query,
        "query_parameters": params,
        "properties": properties
    }

    return res
