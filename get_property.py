import requests
from bs4 import BeautifulSoup
import json
from DB import Database
from Listing import Listing

def get_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")
        soup = json.loads(soup.text)
        return soup
    else:
        print(f"Error {res.status_code}")


active_db = Database("rentals_listings")
url_db = Database('flat_rentals_urls')
urls = url_db.retrieve_all()
active_list = []
i = 0


for url in urls:
    p = get_page(url["url"])
    listing = Listing(p)
    active_db.add_doc(listing.dic)
    i += 1
    print(f"Inserted {i} documents proccesed out of {len(urls)}")
