import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from os import getenv
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List, Optional, Dict

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log the detailed validation error
    logger.error(f"Validation error: {exc}")
    
    # Return the detailed validation errors in the response
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": exc.body,
        }),
    )

# Use MongoDB container's URL (db) provided by Docker Compose
MONGO_URL = getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["main_db"]

# Pydantic model for property input
class Property(BaseModel):
    hash_id: Optional[str] = None
    user_id: Optional[str] = None
    transaction: str  # "rent" or "buy"
    property_type: str
    city: str
    city_part: Optional[str] = None
    street: str
    size_m2: int
    size_kk: Optional[str] = None
    price: Dict
    RK: bool
    contact: Dict
    additional_info: Optional[Dict] = None
    GPS: Dict
    description: Optional[str] = None
    photos: List[str]
    url: Optional[str] = None

# Convert ObjectId to string for returning items
def item_serializer(item):
    item["_id"] = str(item["_id"])
    return item

# Add new property based on transaction type

@app.post("/add")
async def add_property(property: Property):  # Ensure Pydantic validation works
    try:
        # Determine collection based on the transaction type (rent or buy)
        collection_name = "rents" if property.transaction == "rent" else "buys"
        collection = db[collection_name]
        
        # Convert Pydantic model to dictionary
        property_dict = property.dict()
        
        # Insert into the appropriate collection
        result = collection.insert_one(property_dict)

        # Log and return the inserted property ID
        logger.info(f"Inserted property with ID {result.inserted_id} into '{collection_name}' collection")
        return {"message": "Property added successfully", "id": str(result.inserted_id)}

    except Exception as e:
        logger.error(f"Error adding property: {str(e)}")
        if property:
            logger.error(f"Property data at error: {property}")
        raise HTTPException(status_code=500, detail=f"Error adding property: {str(e)}")

# Search items by parameters
@app.get("/{collection_name}")
async def find_by_parameter(
    collection_name: str,
    id: Optional[str] = None,
    property_type: Optional[str] = None,
    city: Optional[str] = None,
    price: Optional[float] = None,  # Either price_per_month for rents or price_total for buys
    size_m2: Optional[int] = None,
    index: Optional[int] = 0,  # Pagination index
    floor: Optional[int] = None,
    garden_size_m2: Optional[int] = None,  # Specific to houses
    bedrooms: Optional[int] = None,  # For any property type
    garage: Optional[bool] = None,  # Specific to houses
    balcony: Optional[bool] = None,  # Common for flats
    furnished: Optional[bool] = None  # For rents, whether the property is furnished
):
    # Choose the collection based on the collection_name (rents or buys)
    collection = db[collection_name]
    logger.info(f"Searching items in collection '{collection_name}' with provided parameters")

    # Build the dynamic query
    query = {}

    # Add filters dynamically
    if id:
        query["_id"] = ObjectId(id)  # Search by MongoDB ObjectId
    if property_type:
        query["property_type"] = property_type
    if city:
        query["city"] = city
    if price is not None:
        # Choose appropriate price field based on the collection (rents vs buys)
        price_field = "price_per_month" if collection_name == "rents" else "price_total"
        query[price_field] = price
    if size_m2 is not None:
        query["size_m2"] = size_m2
    if floor is not None:
        query["additional_info.floor"] = floor
    if garden_size_m2 is not None:
        query["additional_info.garden_size_m2"] = garden_size_m2
    if bedrooms is not None:
        query["additional_info.bedrooms"] = bedrooms
    if garage is not None:
        query["additional_info.garage"] = garage
    if balcony is not None:
        query["additional_info.balcony"] = balcony
    if furnished is not None:
        query["additional_info.furnished"] = furnished

    logger.info(f"Query built: {query}")

    try:
        # Pagination logic: return 50 results per index
        PAGE_SIZE = 50
        skip_count = index * PAGE_SIZE  # Skip based on the index
        results = list(collection.find(query).skip(skip_count).limit(PAGE_SIZE))

        logger.info(f"Found {len(results)} items matching the parameters (page {index})")
        return {"items": [item_serializer(item) for item in results]}
    except Exception as e:
        logger.error(f"Error searching items: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching items")
