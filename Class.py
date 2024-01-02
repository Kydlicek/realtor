from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import json
import time as tm


class Scrape:
    def __init__(self, category_main, category_type, db_collection_name):
        self.category_main = category_main
        self.category_type = category_type
        self.page_num = 1
        self.per_page = 60
        # self.db = Database(db_collection_name)
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
        # self.db.insert_many(self.all_props)
        print(f"Inserted {len(self.all_props)} documents into database")


class RealEstateListing:
    def __init__(self, data):
        self.seo = data["seo"]
        self.hash_id = data["hash_id"]
        self.price = data["price"]
        self.url = f"https://www.sreality.cz/api/cs/v2/estates/{self.hash_id}"
        self.dic = {"seo": self.seo, "hash_id": self.hash_id, "url": self.url}


class Database:
    def __init__(self, collection) -> None:
        self.url = "mongodb+srv://cluster0.5tkxvl3.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
        self.client = MongoClient(
            self.url,
            tls=True,
            tlsCertificateKeyFile="realtor\etc\X509-cert-501200003679591988.pem",
        )

        self.q = self.client["app"][collection]

    def get_doc_count(self):
        doc_count = self.q.count_documents({})
        print(doc_count)

    def add_doc(self, doc):
        self.q.insert_one(doc)

    def insert_many(self, docs):
        self.q.insert_many(docs)

    def retrieve_all(self):
        l = []
        a = self.q.find()
        for el in a:
            l.append(el)
        return l

    def find_by_param(self, param):
        a = self.q.find(param)
        for i in a:
            print(i)


class FullEstateLisitng:
    def __init__(self, data):
        self.data = data

        #     #long description
        #     self.description = self.data['text']['value']

        #     #seo quering for target API
        #     self.seo = data['seo']

        #     #short important description
        #     self.meta_description = data['meta_description']

        #     #broker info etc ....
        #     self.x = data['_embedded']

        #     #images list of lists
        #     self.images = self.make_images()

        #     #geolocation
        #     self.coordinates = self.get_coordinates()

        #     #query data
        #     self.recommendations_data = data['recommendations_data']

        #     #value with sell property type size in kk + m2
        #     self.name = data['name']['value']

        #     #cena, poznamka k cene, stav objektu, typ vlastnictvi,plocha topeni, energeticka narocnost, usefull for more info about property
        #     self.items = data['items']

        #     #locality_district_id, filtering value
        #     self.locality_district_id = data['locality_district_id']

        self.dic = {"data": self.data}

    # def get_coordinates(self):
    #     loc = self.data['map']
    #     dic = {'coordinates':[loc['lon'],loc['lat']]}
    #     return dic

    # def make_images(self):      11111111111111
    #     #includes list of images needs filtering
    #     self.x['images']
