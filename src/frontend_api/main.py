import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx  # Use httpx for async requests
from os import getenv
from fastapi.middleware.cors import CORSMiddleware
#from prompt_model import RealEstateParameters, prompt, llm, ChatOpenAI
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Retrieve the DB_API_URL from the environment variable
DB_API_URL = getenv("DB_API_URL")


# Define the Pydantic model for the incoming request
class SearchQuery(BaseModel):
    query: str


# Predefined response for development purposes
ml_recognition = {
    "parsed_query": {
        "city": "Prague",
        "budget": "20000",
        "house_type": "Apartment",
        "size_kk": "2KK",
        "size_m2": "60",
        "filter": "cheapest",
        "page": "1",
    }
}


@app.post("/search")
async def search_properties(search_query: SearchQuery):
    logger.info(f"Received search request with query: {search_query.query}")


    # messages = prompt.apply({"text": text})
    #     # Get response from the language model
    # response = await llm.agenerate(messages)
    try:
        # Send request to db-api asynchronously
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{DB_API_URL}/items")

        # Log the response from db-api
        logger.info(f"Response from db-api: {res.json()['items']}")

        # Handle errors from db-api
        if res.status_code != 200:
            logger.error(f"Error from db-api, status code: {res.status_code}")
            raise HTTPException(
                status_code=res.status_code,
                detail="Error fetching properties from db-api",
            )

        user_msg = {"query": search_query.query, "properties": res.json()["items"]}
        logger.info(f"Sending response to client: {user_msg}")
        return user_msg
    except httpx.RequestError as e:
        logger.error(f"Error connecting to db-api: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error connecting to db-api: {str(e)}"
        )


@app.get("/test")
async def test():
    logger.info("Test endpoint hit")
    return ml_recognition
