import requests
from bs4 import BeautifulSoup
import json
from DB import Database
from S_listing import Listing


def get_page(url):
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ','Referer':url,}
    res = requests.get(url,headers=header)
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

for url in urls:
    print(url['url'])
    p = get_page(url['url'])
    if p != None:
        l = Listing(p)
        dic = l.get_dict()
        print(dic['price'])

        #print(l.get_dict())


