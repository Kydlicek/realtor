import aiohttp
import asyncio
import logging
from DB import Database
from S_listing import Listing
from tasks import check_and_notify_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

active_db = Database("rentals_listings")
urls_db = Database('flat_rentals_urls')
urls = urls_db.find_by_param({"status": "scraped"})
active_list = []

async def fetch(session, url):
    try:
        async with session.get(url['url'], headers={'user-agent': 'Mozilla/5.0'}) as response:
            return await response.json()
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None

async def process_url(url):
    async with aiohttp.ClientSession() as session:
        page_data = await fetch(session, url)
        if page_data:
            try:
                listing = Listing(page_data)
                return listing.get_dict()
            except KeyError as e:
                logger.error(f"KeyError: {e} for URL: {url['url']}")
                return None
    return None

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(url) for url in urls]
        results = await asyncio.gather(*tasks)
        active_list.extend([result for result in results if result])
        
        if active_list:
            active_db.insert_many(active_list)
            logger.info(f"Inserted {len(active_list)} documents into the database")
        else:
            logger.info("No new valid listings to insert into the database")
        
        for url in urls:
            urls_db.update_document_status(url['_id'], 'fetched')
        
        #check_and_notify_users.delay(active_list)  # Use Celery task

if __name__ == "__main__":
    asyncio.run(main())
