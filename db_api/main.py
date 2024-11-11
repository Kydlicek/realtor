import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from os import getenv
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List, Optional, Dict
from models.property import Property

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Use MongoDB container's URL (db) provided by Docker Compose
MONGO_URL = getenv("MONGO_URL")
MONGO_DB_CLIENT = str(getenv("MONGO_DB_CLIENT"))
client = MongoClient(MONGO_URL)
db = client[MONGO_DB_CLIENT]


# Convert ObjectId to string for returning items
def item_serializer(item):
    item["_id"] = str(item["_id"])
    return item


@app.post("/add")
async def add_property(property: Property):
    collection_name = property.property_type
    collection = db[collection_name]
    try:
        property_dict = property.dict()
        result = collection.insert_one(property_dict)
        logger.info(f"Inserted property with ID {result.inserted_id}")
        return {"message": "Property added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error adding property: {str(e)}")
        raise HTTPException(status_code=500, detail="Error adding property.")

# collection name is property type
@app.get("/{collection_name}")
async def find_by_parameter(
    collection_name: str,
    hash_id: Optional[str] = None,
    id: Optional[str] = None,
    property_type: Optional[str] = None,
    transaction: Optional[str] = None,
    city: Optional[str] = None,
    price: Optional[float] = None,
    size_m2: Optional[int] = None,
    rk: Optional[bool] = None,
):

    collection = db[collection_name]
    query = {}

    if id:
        query["_id"] = ObjectId(id)
    if hash_id:
        query["hash_id"] = hash_id
    if property_type:
        query["property_type"] = property_type
    if transaction:
        query["transaction"] = transaction
    if city:
        query["city"] = city
    if rk is not None:
        query["rk"] = rk
    if size_m2 is not None:
        query["size_m2"] = {"$lt": int(size_m2)}  
    if price is not None:
        query["price"] = {"$lte": int(price)}  # Ensure `price` is converted to int in MongoDB

    # Fetch and process results
    results = collection.find(query)
    results_list = [dict(result, _id=str(result["_id"])) for result in results]
    if not results_list:
        raise HTTPException(status_code=404, detail="No items found matching the query parameters.")
    
    return {"results": results_list}