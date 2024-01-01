from pymongo import MongoClient

class RealEstateListing:
    def __init__(self, data):
        self.seo = data['seo']
        self.hash_id = data['hash_id']
        self.price = data['price']
        self.url = f'https://www.sreality.cz/api/cs/v2/estates/{self.hash_id}'
        self.dic = {'seo':self.seo,'hash_id':self.hash_id,'url':self.url}


class Database:
    def __init__(self,db,collection) -> None:
        self.url = "mongodb+srv://cluster0.5tkxvl3.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
        self.client = MongoClient(self.url,
                     tls=True,
                     tlsCertificateKeyFile='app/etc/X509-cert-501200003679591988.pem')
        
        self.q = self.client[db][collection]
        
    def get_doc_count(self):
        doc_count = self.q.count_documents({})
        print(doc_count)
    
    def add_doc(self,doc):
        self.q.insert_one(doc)
    
    def insert_many(self,docs):
        self.q.insert_many(docs)
    
    def retrieve_all(self):
        l = []
        a = self.q.find()
        for el in a:
            l.append(el)
        return l

    def find_by_param(self,param):
        a = self.q.find(param)
        for i in a:
            print(i)

class FullEstateLisitng:
    def __init__(self,data):
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

        self.dic = {'data':self.data}

    # def get_coordinates(self):
    #     loc = self.data['map']
    #     dic = {'coordinates':[loc['lon'],loc['lat']]}
    #     return dic
    
    # def make_images(self):      11111111111111  
    #     #includes list of images needs filtering
    #     self.x['images']