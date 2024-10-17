from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import logging
from os import getenv

# Setup logging
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Define the request schema
class SearchQuery(BaseModel):
    query: str

# Load the trained BERT model and tokenizer from the 'results' directory
model = BertForSequenceClassification.from_pretrained("./saved_model")
tokenizer = BertTokenizer.from_pretrained("./saved_model")

DB_API_URL = getenv("DB_API_URL")
# Your existing properties collection (this will be your db-api endpoint)
props_collection = f"{DB_API_URL}/properties"



@app.post("/search")
async def search_properties(query: SearchQuery):
    logger.info(f"Received search request with query: {query.query}")

    # Tokenize the user input query
    inputs = tokenizer(query.query, return_tensors="pt", truncation=True, padding=True)

    # Use the BERT model to get predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract the predicted class labels
    predicted_labels = torch.argmax(outputs.logits, dim=-1).tolist()

    # Log the predicted labels
    logger.info(f"Predicted labels from BERT: {predicted_labels}")

    # Modify the query using the predicted labels (e.g., based on model output)
    # You can map predicted_labels to actual category names here if needed
    # Example: Modify the query to include additional filters
    # This part depends on how your model is trained and what labels it outputs
    modified_query = {
        "original_query": query.query,
        "bert_labels": predicted_labels  # You can replace this with category names
    }

    # Now proceed with the existing logic to send the modified query to db-api
    try:
        # Send request to db-api asynchronously with the modified query
        async with httpx.AsyncClient() as client:
            res = await client.get(props_collection)

        # Log the response from db-api
        logger.info(f"Response from db-api: {res.json()['items']}")

        # Handle errors from db-api
        if res.status_code != 200:
            logger.error(f"Error from db-api, status code: {res.status_code}")
            raise HTTPException(
                status_code=res.status_code,
                detail="Error fetching properties from db-api",
            )

        # Return the combined result
        user_msg = {"query": modified_query, "properties": res.json()["items"]}
        logger.info(f"Sending response to client: {user_msg}")
        return user_msg

    except httpx.RequestError as e:
        logger.error(f"Error connecting to db-api: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error connecting to db-api: {str(e)}"
        )
