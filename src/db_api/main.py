import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from os import getenv
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Use MongoDB container's URL (db) provided by Docker Compose
MONGO_URL = getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["main_db"]
collection = db["properties"]


# Pydantic models for data validation
class Item(BaseModel):
    name: str
    address: str
    coordinates: List[float]
    price: str
    prop_type: str
    images: List[str]
    prop_size_kk: int
    prop_size_m2: int
    energy_class: str
    rk: str
    floor: int
    parking: int
    elevator: str
    features: List[str]
    neighborhood_description: str
    amenities: List[str]
    transport: List[str]
    average_rent: str
    security_deposit: str
    agency_fee: str
    rent: str
    utilities: str


# Convert ObjectId to string for returning items
def item_serializer(item):
    item["_id"] = str(item["_id"])
    return item


# Retrieve all items from the collection
@app.get("/items/{collection_name}")
async def get_items(collection_name: str):
    logger.info("Fetching all items from MongoDB")
    try:
        items = list(collection_name.find())
        logger.info(f"Retrieved {len(items)} items")
        return {"items": [item_serializer(item) for item in items]}
    except Exception as e:
        logger.error(f"Failed to retrieve items: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve items")


# Insert a new item into the collection
@app.post("/items/{collection_name}")
async def create_item(collection_name: str, item: object):
    # Get the collection dynamically based on the URL path parameter
    collection = db[collection_name]

    logger.info(f"Inserting new item into collection '{collection_name}': {item}")
    try:
        item_dict = item.dict()
        result = collection.insert_one(item_dict)
        logger.info(f"Inserted item with id: {str(result.inserted_id)}")
        return {"_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Failed to insert item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to insert item")



# Retrieve an item by ID
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


# Delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    logger.info(f"Deleting item with id: {item_id}")
    try:
        result = collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            logger.info(f"Item with id {item_id} deleted")
            return {"message": "Item deleted"}
        logger.warning(f"Item with id {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid item ID")


# Update an item's status by ID
@app.put("/items/{item_id}/status")
async def update_item_status(item_id: str, new_status: str):
    logger.info(f"Updating status of item {item_id} to {new_status}")
    try:
        result = collection.update_one(
            {"_id": ObjectId(item_id)}, {"$set": {"status": new_status}}
        )
        if result.matched_count == 1:
            logger.info(f"Item {item_id} status updated to {new_status}")
            return {"message": f"Item {item_id} status updated"}
        else:
            logger.warning(f"Item with id {item_id} not found")
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error updating item status: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid item ID")


@app.get("/items/search/")
async def find_by_parameter(
    id: int = None,
    name: str = None,
    address: str = None,
    price: str = None,
    prop_type: str = None,
    energy_class: str = None,
    rk: str = None,
    floor: int = None,
    parking: int = None,
    elevator: str = None,
    features: List[str] = None,
    neighborhood_description: str = None,
    average_rent: str = None,
):
    logger.info(f"Searching items with provided parameters")
    query = {}

    # Dynamically build the query based on provided parameters
    if id:
        query["id"] = id
    if name:
        query["name"] = name
    if address:
        query["address"] = address
    if price:
        query["price"] = price
    if prop_type:
        query["prop_type"] = prop_type
    if energy_class:
        query["energy_class"] = energy_class
    if rk:
        query["rk"] = rk
    if floor:
        query["floor"] = floor
    if parking:
        query["parking"] = parking
    if elevator:
        query["elevator"] = elevator
    if features:
        query["features"] = {"$all": features}  # Use $all for list matching
    if neighborhood_description:
        query["neighborhood_description"] = neighborhood_description
    if average_rent:
        query["average_rent"] = average_rent

    logger.info(f"Query built: {query}")

    try:
        # Fetch results based on the dynamic query
        results = list(collection.find(query))
        logger.info(f"Found {len(results)} items matching the parameters")
        return {"items": [item_serializer(item) for item in results]}
    except Exception as e:
        logger.error(f"Error searching items: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching items")
