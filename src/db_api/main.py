import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from os import getenv
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List, Optional,Dict

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Use MongoDB container's URL (db) provided by Docker Compose
MONGO_URL = getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["main_db"]



# Convert ObjectId to string for returning items
def item_serializer(item):
    item["_id"] = str(item["_id"])
    return item



@app.post("/{collection_name}")
async def save_to_db(collection_name: str, obj: Dict):
    logger.info(f"Saving: {obj} to {collection_name}")
    try:
        # Insert the object into the specified collection
        result = db[collection_name].insert_one(obj)
        
        # Log the inserted ID
        logger.info(f"Inserted object with id: {str(result.inserted_id)}")
        
        # Return the inserted ID as a response
        return {"_id": str(result.inserted_id)}
    
    except Exception as e:
        # Log the error and raise an HTTP exception
        logger.error(f"Failed to insert object: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to insert object")




# Retrieve an item by ID
@app.get("/{collection_name}/{item_id}")
async def get_item(collection_name: str, item_id: str):
    collection = db[collection_name]
    logger.info(f"Fetching item with id: {item_id} from collection '{collection_name}'")
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
@app.delete("/{collection_name}/{item_id}")
async def delete_item(collection_name: str, item_id: str):
    collection = db[collection_name]
    logger.info(f"Deleting item with id: {item_id} from collection '{collection_name}'")
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
@app.put("/{collection_name}/{item_id}/status")
async def update_item_status(collection_name: str, item_id: str, new_status: str):
    collection = db[collection_name]
    logger.info(
        f"Updating status of item {item_id} in collection '{collection_name}' to {new_status}"
    )
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


# Search items by parameters
@app.get("/{collection_name}")
async def find_by_parameter(
    collection_name: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    address: Optional[str] = None,
    price: Optional[str] = None,
    prop_type: Optional[str] = None,
    energy_class: Optional[str] = None,
    rk: Optional[str] = None,
    floor: Optional[int] = None,
    parking: Optional[int] = None,
    elevator: Optional[str] = None,
    features: Optional[List[str]] = None,
    neighborhood_description: Optional[str] = None,
    average_rent: Optional[str] = None,
    status: Optional[str] = None,
):
    collection = db[collection_name]
    logger.info(
        f"Searching items in collection '{collection_name}' with provided parameters"
    )
    query = {}

    # Dynamically build the query based on provided parameters
    if id:
        query["_id"] = ObjectId(id)  # Expecting MongoDB ObjectId
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
    if floor is not None:
        query["floor"] = floor
    if parking is not None:
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
