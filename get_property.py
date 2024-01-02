import requests
from bs4 import BeautifulSoup
import json
import time as tm
from Class import Database


def get_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")
        soup = json.loads(soup.text)
        return soup
    else:
        print(f"Error {res.status_code}")


active_db = Database("real_estate_app", "active_listings")
url_db = Database("real_estate_app", "first_scrape")
urls = url_db.retrieve_all()
active_list = []
i = 0


for url in urls:
    p = get_page(url["url"])
    dic = {"data": p}
    active_db.add_doc(p)
    i += 1
    print(f"Inserted {i} documents proccesed out of {len(urls)}")
