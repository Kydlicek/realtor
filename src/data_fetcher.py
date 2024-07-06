import requests
import json
from DB import Database
from S_listing import Listing
import logging
from multiprocessing import Pool, cpu_count
from bson.objectid import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

active_db = Database("rentals_listings")
urls_db = Database('flat_rentals_urls')
urls = urls_db.find_by_param({"status": "scraped"})
active_list = []

def get_page(url):
    """
    Sends a GET request to the sreality.cz API and returns the parsed response.

    Parameters:
    - url (str): The URL to send the GET request to.

    Returns:
    - dict: Parsed JSON response from the API.
    """
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
              'Referer': url}
    try:
        res = requests.get(url, headers=header)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def process_url(url):
    """
    Processes a single URL: fetches the page, creates a Listing object, and returns the listing dictionary.

    Parameters:
    - url (dict): A dictionary containing the URL to be processed.

    Returns:
    - dict: The listing dictionary if the page was fetched successfully, otherwise None.
    """
    page_data = get_page(url['url'])
    if page_data:
        try:
            listing = Listing(page_data)
            return listing.get_dict()
        except KeyError as e:
            logger.error(f"KeyError: {e} for URL: {url['url']}")
            return None
    return None

def main():
    # Use multiprocessing to process the URLs
    with Pool(cpu_count()) as pool:
        results = pool.map(process_url, urls)

    # Filter out None results and add the valid listings to the active_list
    active_list.extend([result for result in results if result])

    # Insert the listings into the database
    if active_list:
        active_db.insert_many(active_list)
        logger.info(f"Inserted {len(active_list)} documents into the database")
    else:
        logger.info("No valid listings to insert into the database")

    # Update the status of processed URLs to "fetched"
    for url in urls:
        urls_db.update_document_status(ObjectId(url['_id']), 'fetched')

if __name__ == "__main__":
    main()
