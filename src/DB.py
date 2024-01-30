from pymongo import MongoClient

class Database:
    def __init__(self, collection) -> None:
        self.url = 'mongodb+srv://cluster0.5tkxvl3.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority'
        self.client = MongoClient(
            self.url,
            tls=True,
            tlsCertificateKeyFile="./etc/X509-cert-3739710124139658835.pem",
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