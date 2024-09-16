import logging
from fastapi import FastAPI
from pymongo import MongoClient
from os import getenv
from bson.objectid import ObjectId  # Ensure ObjectId is imported
from props import properties  # Assuming this imports a list of property data

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Use MongoDB container's URL (db) provided by Docker Compose
MONGO_URL = getenv("MONGO_URL", "mongodb://db:27017/")
client = MongoClient(MONGO_URL)
db = client["your_database"]
collection = db["your_collection"]


@app.get("/items")
async def get_items():
    logger.info("Fetching all items from MongoDB")
    items = list(collection.find({}, {"_id": 1, "name": 1}))  # Fetch only name and _id
    logger.info(f"Retrieved {len(items)} items from MongoDB")
    return {"items": items}


@app.get("/items/{item_id}")
async def get_item(item_id: str):
    logger.info(f"Fetching item with id: {item_id}")
    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            logger.info(f"Item found: {item}")
            return {"item": item}
        logger.warning(f"Item with id {item_id} not found")
        return {"error": "Item not found"}
    except Exception as e:
        logger.error(f"Error fetching item: {str(e)}")
        return {"error": "Invalid item ID"}


@app.post("/items")
async def create_item(item: dict):
    logger.info(f"Inserting new item into the database: {item}")
    result = collection.insert_one(item)
    logger.info(f"Inserted item with id: {str(result.inserted_id)}")
    return {"_id": str(result.inserted_id)}


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    logger.info(f"Deleting item with id: {item_id}")
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        logger.info(f"Item with id {item_id} deleted")
        return {"message": "Item deleted"}
    logger.warning(f"Item with id {item_id} not found for deletion")
    return {"error": "Item not found"}
