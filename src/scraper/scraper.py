import sys
from os import getenv
import logging
from bs4 import BeautifulSoup
import json
import time as tm
import requests
import aiohttp
from itertools import islice  # Correct import
from models import Listing

# from dotenv import load_dotenv

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# load_dotenv()


class Scraper:
    """
    Class for scraping real estate listings from the sreality.cz website.
    """

    def __init__(self, category_main, category_type):
        """
        Initializes a Scrape object.

        Parameters:
        - category_main (int): Main category of the real estate (1 Byty, 2 Domy, 3 Pozemky, 4 Komercni, 5 Ostatni)
        - category_type (int): Type of real estate transaction (1 Prodej, 2 Pronajem)
        - db_collection_name (str): Name of the collection in the database to store the scraped data.
        """
        self.category_main = category_main
        self.category_type = category_type
        self.page_num = 1
        self.per_page = 60
        self.api_url = getenv("DB_API_URL")
        # self.api_url = "http://localhost:8000"
        logger.info(f"API URL: {self.api_url}")
        self.urls_collection = "scraped_urls"
        self.props_collection = "properties"
        self.all_props = []
        self.update_url()
        self.scraped_urls = self.pull_scraped()
        self.res_lenght = self.get_page(self.url)["result_size"]

    def update_url(self):
        """
        Update the URL with the current page number and timestamp.
        """
        self.tms = tm.time()
        self.url = (
            f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb={self.category_main}"
            f"&category_type_cb={self.category_type}&no_auction=1&no_shares=1"
            f"&page={self.page_num}&per_page={self.per_page}&tms={self.tms}"
        )

    def pull_scraped(self):
        try:
            response = requests.get(f"{self.api_url}/items/{self.urls_collection}")

            return response.json()["items"]
        except:
            logger.error("Failed to pull scraped urls")
            return []

    def get_page(self, url):
        """
        Sends a GET request to the sreality.cz API and returns the parsed response.

        Parameters:
        - url (str): The URL to send the GET request to.

        Returns:
        - dict: Parsed JSON response from the API.
        """
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": url,
        }
        try:
            res = requests.get(url, headers=header)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def scrape_pages(self, start_page, end_page):
        """
        Scrapes real estate listings from specified pages and stores them in the 'all_props' list.

        Parameters:
        - start_page (int): Starting page number for scraping.
        - end_page (int): Ending page number for scraping.
        """
        for i in range(start_page, end_page):
            self.page_num = i
            self.update_url()
            soup = self.get_page(self.url)
            if not soup:
                continue

            props = soup["_embedded"]["estates"]

            for prop in props:
                prop = self.make_listing(prop)
                if self.prop_exists(prop["hash_id"]):
                    return
                else:
                    self.all_props.append(prop)
            logger.info(
                f"Scraped page {self.page_num} of {end_page - 1} || Listings: {len(self.all_props)}"
            )

    def prop_exists(self, hash_id):
        for el in self.scraped_urls:
            if el["hash_id"] == hash_id:
                return True
        return False

    def make_listing(self, data):
        seo = data["seo"]
        hash_id = str(data["hash_id"])
        url = f"https://www.sreality.cz/api/cs/v2/estates/{hash_id}"
        return {"hash_id": hash_id, "url": url, "status": "pending"}

    def scrape_all(self):
        """
        Scrapes all pages of real estate listings and stores them in the 'all_props' list.
        """
        pages_to_scrape = self.res_lenght // self.per_page + 1
        self.scrape(1, pages_to_scrape)

    def save_scraped(self):
        for el in self.all_props:
            response = requests.post(
                f"{self.api_url}/urls/{self.urls_collection}",
                json=el,
            )
            logger.info(f"{response.status_code, response.text}")

    def procces_props(self):
        pass
        # for el in self.all_props:
        #     prop = self.process_url(el)
        #     response = requests.post(
        #         f"{self.api_url}/items/{self.props_collection}",
        #         json=prop,
        #     )
        #     logger.info(f"prop_created and sent to DB {response}")

    def fetch(self, session, url):
        try:
            with session.get(
                url["url"], headers={"user-agent": "Mozilla/5.0"}
            ) as response:
                return response.json()
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    def process_url(self, url):
        try:
            response = requests.get(url["url"], headers={"user-agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise an exception for bad responses
            page_data = response.json()

            if page_data:
                return Listing(page_data).get_dict()
        except KeyError as e:
            logger.error(f"KeyError: {e} for URL: {url['url']}")
        except requests.RequestException as e:
            logger.error(f"Request failed: {e} for URL: {url['url']}")

            return None


if __name__ == "__main__":
    flat_rentals = Scraper(1, 2)
    flat_rentals.scrape_pages(1, 2)
    flat_rentals.save_scraped()
    flat_rentals.procces_props()
