import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from os import getenv
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import List

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Use MongoDB container's URL (db) provided by Docker Compose
MONGO_URL = getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["your_database"]
collection = db["your_collection"]

# Pydantic models for data validation


class Item(BaseModel):
    id: int
    name: str
    address: str
    coordinates: List[float]
    price: str
    prop_type: str
    images: List[str]
    prop_size_kk: int
    prop_size_m2: int
    energy_class: str
    rk: str  # Store as string since the input has "True" as a string
    floor: int
    parking: int
    elevator: str  # Store as string since the input has "True" as a string
    features: List[str]
    neighborhood_description: str
    amenities: List[str]
    transport: List[str]
    average_rent: str
    Security_Deposit: str  # Added capitalization to avoid space in key
    Agency_Fee: str  # Added capitalization to avoid space in key
    Rent: str
    Utilities: str


# Convert ObjectId to string for returning items
def item_serializer(item):
    item["_id"] = str(item["_id"])
    return item


@app.get("/items")
async def get_items():
    logger.info("Fetching all items from MongoDB")
    items = list(collection.find({}, {"_id": 1, "name": 1}))  # Fetch only _id and name
    logger.info(f"Retrieved {len(items)} items from MongoDB")
    return {"items": [item_serializer(item) for item in items]}


@app.get("/items/{item_id}")
async def get_item(item_id: str):
    logger.info(f"Fetching item with id: {item_id}")
    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            logger.info(f"Item found: {item}")
            return {"item": item_serializer(item)}
        logger.warning(f"Item with id {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error fetching item: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid item ID")


@app.post("/items")
async def create_item(item: Item):
    logger.info(f"Inserting new item into the database: {item}")
    item_dict = item.dict()  # Convert Pydantic model to dict
    result = collection.insert_one(item_dict)
    logger.info(f"Inserted item with id: {str(result.inserted_id)}")
    return {"_id": str(result.inserted_id)}


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    logger.info(f"Deleting item with id: {item_id}")
    try:
        result = collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            logger.info(f"Item with id {item_id} deleted")
            return {"message": "Item deleted"}
        logger.warning(f"Item with id {item_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid item ID")
