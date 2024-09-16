from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx  # Use httpx for async requests
from os import getenv
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/search")
async def search_properties(query: str):
    try:
        # Send request to db-api asynchronously
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{DB_API_URL}/items")

        # Handle errors from db-api
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail="Error fetching properties from db-api",
            )

        user_msg = {"query": query, "properties": res.json()}
        return user_msg
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to db-api: {str(e)}"
        )


@app.get("/test")
async def test():
    return ml_recognition
