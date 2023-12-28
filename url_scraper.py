import requests
from bs4 import BeautifulSoup
import json
import time as tm
from Class import RealEstateListing, Database




class RealEstateListing:
    def __init__(self, data):
        self.seo = data['seo']
        self.hash_id = data['hash_id']
        self.price = data['price']
        self.url = f'https://www.sreality.cz/api/cs/v2/estates/{self.hash_id}'
        self.dic = {'seo':self.seo,'hash_id':self.hash_id,'url':self.url}



def get_page(url):
    
    res = requests.get(url)
    if res.status_code == 200:
            soup = BeautifulSoup(res.content,'html.parser')
            soup = json.loads(soup.text)
            return soup
    else:
        print(f'Error {res.status_code}')


def get_res_lenght():
    p = get_page(url)
    return p['result_size']







db = Database('real_estate_app','first_scrape')

#category_main = 1 Byty, 2 Domy, 3 Pozemky, 4 Komercni, 5 Ostatni
category_main = 1
#category_type = 1 Prodej, 2 Pronajem
category_type = 1
#page_num = 1 = cislo stranky
page_num = 1
#per_page = 60 = pocet inzeratu na strance
per_page = 60
#aktualni cas v milisekundach
tms = tm.time()


#url = f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb={category_main}&category_type_cb={category_type}&no_auction=1&no_shares=1&page={page_num}&per_page={per_page}&tms={tms}'
url = f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb={category_main}&category_type_cb={category_type}&no_auction=1&no_shares=1&page={page_num}&per_page={per_page}&tms={tms}'

all_props = []
res_lenght = get_res_lenght()
pages_to_scrape = res_lenght // per_page + 1

for i in range(1,pages_to_scrape+1):
    print(f'Scraping page {i} of {pages_to_scrape}')
    page_num = i
    soup = get_page(url)
    props  = soup['_embedded']['estates']
    for prop in props:
        prop = RealEstateListing(prop)
        all_props.append(prop.dic)

db.insert_many(all_props)
print(f'Inserted {len(all_props)} documents into database')