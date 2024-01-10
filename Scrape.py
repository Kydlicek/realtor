from bs4 import BeautifulSoup
import json
import time as tm
from DB import Database
import requests

# category_main = 1 Byty, 2 Domy, 3 Pozemky, 4 Komercni, 5 Ostatni
# category_type = 1 Prodej, 2 Pronajem
# db_collection_name = nazev kolekce v DB = "flat_rentals_urls"

# aktualni cas v milisekundach
tms = tm.time()
class Scrape:
    def __init__(self, category_main, category_type, db_collection_name):
        self.category_main = category_main
        self.category_type = category_type
        # page_num = 1 = cislo stranky
        self.page_num = 1
        # per_page = 60 = pocet inzeratu na strance
        self.per_page = 60
        self.db = Database(db_collection_name)
        self.tms = tm.time()
        self.url = f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb={category_main}&category_type_cb={category_type}&no_auction=1&no_shares=1&page={self.page_num}&per_page={self.per_page}&tms={self.tms}"
        self.all_props = []
        self.res_lenght = self.get_page()["result_size"]

    # function to get page
    def get_page(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            soup = json.loads(soup.text)
            return soup
        else:
            print(f"Error {res.status_code}")

    # function to scrape
    def scrape(self, start_page, end_page):
        # loop through pages
        for i in range(start_page, end_page):
            self.page_num = i
            soup = self.get_page()
            props = soup["_embedded"]["estates"]

            # page return 60 listing > loop iteration to get all listings on page
            for prop in props:
                prop = RealEstateListing(prop)
                self.all_props.append(prop.dic)
            print(
                f"scraped page {self.page_num} of {end_page}|| listings: {len(self.all_props)}"
            )

    # function to scrape all
    def scrape_all(self):
        pages_to_scrape = self.res_lenght // self.per_page + 1
        self.scrape(1, pages_to_scrape)

    # function to add results to db
    def add_to_db(self):
        # insert all properties into database
        self.db.insert_many(self.all_props)
        print(f"Inserted {len(self.all_props)} documents into database")

#format of listing
class RealEstateListing:
    def __init__(self, data):
        self.seo = data["seo"]
        self.hash_id = data["hash_id"]
        self.price = data["price"]
        self.url = f"https://www.sreality.cz/api/cs/v2/estates/{self.hash_id}"
        self.dic = {"seo": self.seo, "hash_id": self.hash_id, "url": self.url}