import os
import logging
import json
import time as tm
import requests
import pika
import time

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.WARNING)

# RabbitMQ settings
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
QUEUE_NAME = os.getenv("QUEUE_NAME")
DB_API_URL = os.getenv("DB_API_URL")

SCRAPING_INTERVAL = os.getenv("SCRAPING_INTERVAL")
SCRAPE_ALL = os.getenv("SCRAPE_ALL", "false").lower() == "true"
PROPERTY_TYPE = int(os.getenv("PROPERTY_TYPE", 1))
TRANSACTION_TYPE = int(os.getenv("TRANSACTION_TYPE", 2))


class Scraper:
    def __init__(self, category_main, category_type):
        self.connection = None
        self.channel = None
        self.category_main = category_main
        self.category_type = category_type
        self.page_num = 1
        self.per_page = 60
        self.all_props = []
        self.update_url()

        page_info = self.get_page(self.url)
        self.res_length = page_info["result_size"] if page_info else 0

    def update_url(self):
        self.tms = tm.time()
        self.url = (
            f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb={self.category_main}"
            f"&category_type_cb={self.category_type}&no_auction=1&no_shares=1"
            f"&page={self.page_num}&per_page={self.per_page}&tms={self.tms}"
        )

    def get_page(self, url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": url,
        }
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def hash_exists(self, hash_id, property_type):
        response = requests.get(
            f"{DB_API_URL}/{property_type}", params={"hash_id": hash_id}
        )
        return response.status_code == 200

    def connect_to_rabbitmq(self):
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
            logger.info("Persistent connection to RabbitMQ established.")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"RabbitMQ connection failed: {e}")
            raise

    def scrape_pages(self, start_page, end_page):
        for i in range(start_page, end_page):
            self.page_num = i
            self.update_url()
            page_data = self.get_page(self.url)
            if not page_data:
                continue

            props = page_data["_embedded"]["estates"]
            for prop in props:
                hash_id = prop["hash_id"]
                url = f"https://www.sreality.cz/api/cs/v2/estates/{hash_id}"
                property_type = "flats" if self.category_main == 1 else "houses"
                transaction = "rents" if self.category_type == 2 else "buys"

                if not self.hash_exists(hash_id, property_type):
                    obj = {
                        "property_type": property_type,
                        "transaction": transaction,
                        "url": url,
                        "hash_id": hash_id,
                    }

                    self.all_props.append(obj)
                else:

                    pass

            logger.info(
                f"Scraped page {self.page_num} of {end_page - 1} || Listings: {len(self.all_props)}"
            )

    def scrape_all(self):
        pages_to_scrape = self.res_length // self.per_page + 1
        self.scrape_pages(1, pages_to_scrape)

    def wait_for_rabbitmq_connection(self, max_retries=10, delay=10):
        retries = 0
        while retries < max_retries:
            try:
                credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOST, credentials=credentials
                    )
                )
                connection.close()
                logger.info("Successfully connected to RabbitMQ.")
                return True
            except pika.exceptions.AMQPConnectionError as e:
                retries += 1
                logger.warning(
                    f"Failed to connect to RabbitMQ. Retrying in {delay} seconds... (Attempt {retries}/{max_retries})"
                )
                time.sleep(delay)

        logger.error(f"Failed to connect to RabbitMQ after {max_retries} retries.")
        return False

    def send_to_queue(self):
        for url in self.all_props:
            self.send_to_rabbitmq(url)

    def send_to_rabbitmq(self, url):
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=json.dumps(url),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            logger.info(f"Sent URL to RabbitMQ: {url}")
        except pika.exceptions.AMQPChannelError as e:
            logger.error(f"Failed to send message to RabbitMQ: {e}")

    def run(self):
        self.connect_to_rabbitmq()
        self.scrape_all()
        self.send_to_queue()


if __name__ == "__main__":
    while True:
        # Determine if scraping all or specific types based on SCRAPE_ALL
        if SCRAPE_ALL:
            parameters = [
                (1, 2),  # Flats for rent
                (1, 1),  # Flats for buy
                (2, 1),  # Houses for buy
                (2, 2),  # Houses for rent
            ]
        else:
            parameters = [(PROPERTY_TYPE, TRANSACTION_TYPE)]

        for param1, param2 in parameters:
            scraper = Scraper(param1, param2)
            if scraper.wait_for_rabbitmq_connection():
                scraper.run()
            else:
                logger.error("Could not establish connection to RabbitMQ. Exiting.")

        logging.info(f"Scraping finished; now taking {SCRAPING_INTERVAL} sec nap")
        time.sleep(SCRAPING_INTERVAL)  # Wait before the next run
