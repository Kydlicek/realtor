from fastapi import FastAPI
from pydantic import BaseModel
import requests
from os import getenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Retrieve the DB_API_URL from the environment variable
DB_API_URL = getenv("DB_API_URL", "http://localhost:8000")


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
    # Send request to db-api
    res = requests.get(f"{DB_API_URL}/items")
    user_msg = {"query": ml_recognition, "properties": res.json()}
    return user_msg
