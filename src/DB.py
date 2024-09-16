from pymongo import MongoClient
import logging
import os


class Database:
    def __init__(self, collection) -> None:
        """
        Initializes a Database object.

        Parameters:
        - collection (str): The name of the collection in the MongoDB database.
        """
        # self.url = 'mongodb+srv://cluster0.5tkxvl3.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority'

        self.url = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.cert = os.getenv("MONGO_CERT", None)

        if self.cert:
            # If a certificate is provided, connect using TLS
            self.client = MongoClient(
                self.url,
                tls=True,
                tlsCertificateKeyFile=self.cert,
            )
        else:
            # Connect without TLS if no certificate is provided
            self.client = MongoClient(self.url)

        self.q = self.client["app"][collection]
        self.logger = logging.getLogger(__name__)

    def get_doc_count(self):
        """
        Returns the number of documents in the collection.
        """
        try:
            doc_count = self.q.count_documents({})
            self.logger.info(f"Document count: {doc_count}")
            return doc_count
        except Exception as e:
            self.logger.error(f"Failed to get document count: {e}")

    def add_doc(self, doc):
        """
        Inserts a single document into the collection.

        Parameters:
        - doc (dict): The document to insert.
        """
        try:
            self.q.insert_one(doc)
            self.logger.info("Inserted one document successfully")
        except Exception as e:
            self.logger.error(f"Failed to insert document: {e}")

    def insert_many(self, docs):
        """
        Inserts multiple documents into the collection.

        Parameters:
        - docs (list): A list of documents to insert.
        """
        try:
            self.q.insert_many(docs)
            self.logger.info(f"Inserted {len(docs)} documents successfully")
        except Exception as e:
            self.logger.error(f"Failed to insert multiple documents: {e}")

    def retrieve_all(self):
        """
        Retrieves all documents from the collection.

        Returns:
        - list: A list of all documents in the collection.
        """
        try:
            l = list(self.q.find())
            self.logger.info(f"Retrieved {len(l)} documents successfully")
            return l
        except Exception as e:
            self.logger.error(f"Failed to retrieve documents: {e}")
            return []

    def find_by_param(self, param):
        """
        Finds documents in the collection that match the given parameter.

        Parameters:
        - param (dict): The parameter to match documents.

        Returns:
        - list: A list of matching documents.
        """
        try:
            results = list(self.q.find(param))
            self.logger.info(f"Found {len(results)} documents matching the parameter")
            return results
        except Exception as e:
            self.logger.error(f"Failed to find documents by parameter: {e}")
            return []

    def update_document_status(self, document_id, new_status):
        """
        Updates the status of a document by its ID.

        Parameters:
        - document_id (ObjectId): The ID of the document to update.
        - new_status (str): The new status to set for the document.
        """
        try:
            self.q.update_one({"_id": document_id}, {"$set": {"status": new_status}})
            self.logger.info(f"Updated document {document_id} status to {new_status}")
        except Exception as e:
            self.logger.error(f"Failed to update document status: {e}")


# Usage Example
if __name__ == "__main__":
    db = Database("test_collection")
    print(db.get_doc_count())
    db.add_doc({"name": "John Doe", "age": 30, "status": "scraped"})
    print(db.retrieve_all())
    print(db.find_by_param({"name": "John Doe"}))
