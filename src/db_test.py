import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_client():
    """
    Creates a MongoDB client with TLS/SSL configuration.
    """
    try:
        client = MongoClient(
            'mongodb+srv://cluster0.5tkxvl3.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority',
            tls=True,
            tlsCertificateKeyFile="./etc/X509-cert-3739710124139658835.pem",
        )
        # Test the connection
        client.admin.command('ping')
        logger.info("MongoDB connection established successfully.")
        return client
    except ConnectionFailure as e:
        logger.error(f"Connection failed: {e}")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def main():
    client = create_client()
    if client:
        db = client["app"]
        collection = db["rentals_listings"]
        # Perform your database operations here
        try:
            results = list(collection.find({"status": "scraped"}))
            for result in results:
                print(result)
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")

if __name__ == "__main__":
    main()
