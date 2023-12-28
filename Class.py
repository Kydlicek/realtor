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
    
    def find_by_param(self,param):
        a = self.q.find(param)
        for i in a:
            print(i)