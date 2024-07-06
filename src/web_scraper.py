import logging
from bs4 import BeautifulSoup
import json
import time as tm
from DB import Database
import requests

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:
    """
    Class for scraping real estate listings from the sreality.cz website.
    """

    def __init__(self, category_main, category_type, db_collection_name):
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
        self.db = Database(db_collection_name)
        self.all_props = []
        self.update_url()
        self.res_lenght = self.get_page(self.url)["result_size"]

    def update_url(self):
        """
        Update the URL with the current page number and timestamp.
        """
        self.tms = tm.time()
        self.url = (f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb={self.category_main}"
                    f"&category_type_cb={self.category_type}&no_auction=1&no_shares=1"
                    f"&page={self.page_num}&per_page={self.per_page}&tms={self.tms}")

    def get_page(self, url):
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

    def scrape(self, start_page, end_page):
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
                if self.prop_exists(prop['hash_id']):
                    pass
                else:
                    self.all_props.append(prop)
            logger.info(
                f"Scraped page {self.page_num} of {end_page - 1} || Listings: {len(self.all_props)}"
            )
    def prop_exists(self,hash_id):
        if self.db.find_by_param({"hash_id":hash_id}):
            return True
        else:
            return False
            

        
    def make_listing(self, data):   
        """
        Create a simplified real estate listing from the original data.

        Parameters:
        - data (dict): Original data of a real estate listing.

        Returns:
        - dict: Simplified real estate listing data.
        """
        seo = data["seo"]
        hash_id = data["hash_id"]
        url = f"https://www.sreality.cz/api/cs/v2/estates/{hash_id}"
        return {"seo": seo, "hash_id": hash_id, "url": url, "status":"scraped"}

    def scrape_all(self):
        """
        Scrapes all pages of real estate listings and stores them in the 'all_props' list.
        """
        pages_to_scrape = self.res_lenght // self.per_page + 1
        self.scrape(1, pages_to_scrape)

    def add_to_db(self):
        """
        Inserts all scraped properties into the database.
        """
        if self.all_props:
            self.db.insert_many(self.all_props)
            logger.info(f"Inserted {len(self.all_props)} documents into the database")
        else:
            logger.info("No properties to insert into the database")

if __name__ == "__main__":
    flat_rentals = Scraper(1, 2, 'flat_rentals_urls')
    flat_rentals.scrape(1, 2)
    flat_rentals.add_to_db()
