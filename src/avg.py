import schedule
import time
from pymongo import MongoClient
import logging
from datetime import datetime

# MongoDB configuration
client = MongoClient('mongodb+srv://cluster0.5tkxvl3.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority',
                     tls=True,
                     tlsCertificateKeyFile="./etc/X509-cert-3739710124139658835.pem")
db = client['app']
listings_collection = db['rentals_listings']
average_prices_collection = db['average_prices']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compute_average_prices():
    """
    Computes average prices for flats based on location and size (in square meters).
    Stores the computed average prices in the 'average_prices' collection.
    This function is intended to run once a day.
    """
    try:
        locations = listings_collection.distinct("location.city")
        for location in locations:
            pipeline = [
                {"$match": {"location.city": location}},
                {"$group": {
                    "_id": "$prop_info.size_m2",
                    "average_price": {"$avg": "$price.rent"},
                    "count": {"$sum": 1}
                }}
            ]
            results = list(listings_collection.aggregate(pipeline))
            for result in results:
                average_prices_collection.update_one(
                    {"location": location, "size_m2": result["_id"]},
                    {"$set": {
                        "location": location,
                        "size_m2": result["_id"],
                        "average_price": result["average_price"],
                        "count": result["count"],
                        "last_updated": datetime.utcnow()
                    }},
                    upsert=True
                )
        logger.info("Successfully computed and stored average prices.")
    except Exception as e:
        logger.error(f"Failed to compute average prices: {e}")

# Schedule the job to run once a day
schedule.every().day.at("01:00").do(compute_average_prices)

while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
