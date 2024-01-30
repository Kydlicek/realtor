import requests
from bs4 import BeautifulSoup
import json
from DB import Database
from S_listing import Listing
from web_scraper import Scrape
import logging


active_db = Database("rentals_listings")
url_db = Database('flat_rentals_urls')
urls = url_db.retrieve_all()
active_list = []

for url in urls:

    p = Scrape.get_page(url['url'])
    if p != None:
        l = Listing(p)
        dic = l.get_dict()


