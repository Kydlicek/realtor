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

# RabbitMQ settings
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password')
QUEUE_NAME = 'urls_queue'

class Scraper:
    """
    Class for scraping real estate listings from the sreality.cz website.
    """

    def __init__(self, category_main, category_type):
        """
        Initializes a Scraper object.
        """
        self.category_main = category_main
        self.category_type = category_type
        self.page_num = 1
        self.per_page = 60
        self.api_url = "http://localhost:8000"
        logger.info(f"API URL: {self.api_url}")
        self.all_props = []
        self.update_url()

        page_info = self.get_page(self.url)
        if page_info:
            self.res_length = page_info["result_size"]
        else:
            self.res_length = 0

    def update_url(self):
        """
        Update the URL with the current page number and timestamp.
        """
        self.tms = tm.time()
        self.url = (
            f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb={self.category_main}"
            f"&category_type_cb={self.category_type}&no_auction=1&no_shares=1"
            f"&page={self.page_num}&per_page={self.per_page}&tms={self.tms}"
        )

    def get_page(self, url):
        """
        Sends a GET request to the sreality.cz API and returns the parsed response.
        """
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

    def scrape_pages(self, start_page, end_page):
        """
        Scrapes real estate listings from specified pages and stores them in the 'all_props' list.
        """
        for i in range(start_page, end_page):
            self.page_num = i
            self.update_url()
            soup = self.get_page(self.url)
            if not soup:
                continue

            props = soup["_embedded"]["estates"]
            for prop in props:
                # Only append the URL to the list of properties
                url = f"https://www.sreality.cz/api/cs/v2/estates/{prop['hash_id']}"
                self.all_props.append(url)

            logger.info(
                f"Scraped page {self.page_num} of {end_page - 1} || Listings: {len(self.all_props)}"
            )

    def scrape_all(self):
        """
        Scrapes all pages of real estate listings and stores them in the 'all_props' list.
        """
        pages_to_scrape = self.res_length // self.per_page + 1
        self.scrape_pages(1, pages_to_scrape)

    def wait_for_rabbitmq_connection(self, max_retries=10, delay=10):
        """
        Wait for RabbitMQ to become available by retrying the connection.
        """
        retries = 0
        while retries < max_retries:
            try:
                # Try to establish the connection to RabbitMQ
                credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
                connection.close()  # Close immediately after testing the connection
                logger.info("Successfully connected to RabbitMQ.")
                return True
            except pika.exceptions.AMQPConnectionError as e:
                retries += 1
                logger.warning(f"Failed to connect to RabbitMQ. Retrying in {delay} seconds... (Attempt {retries}/{max_retries})")
                time.sleep(delay)

        logger.error(f"Failed to connect to RabbitMQ after {max_retries} retries.")
        return False

    def send_to_queue(self):
        """
        Send all scraped URLs to RabbitMQ.
        """
        for url in self.all_props:
            try:
                self.send_to_rabbitmq(url)
            except Exception as e:
                logger.error(f"Failed to send URL to RabbitMQ: {url}, Error: {e}")
    
    def send_to_rabbitmq(self, url):
        """
        Sends a URL message to RabbitMQ queue.
        """
        try:
            # Connect to RabbitMQ with credentials
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
            channel = connection.channel()

            # Declare the queue (make sure it's the same as the consumer's)
            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            # Send the URL as the message to the queue
            channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=json.dumps({'url': url}),  # Send only the URL in the message body
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            logger.info(f"Sent URL to RabbitMQ: {url}")

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"RabbitMQ connection failed: {e}")
            raise
        finally:
            if 'connection' in locals():
                connection.close()


if __name__ == "__main__":
    scraper = Scraper(1, 2)

    # Wait for RabbitMQ to become available before starting the scraping process
    if scraper.wait_for_rabbitmq_connection():
        scraper.scrape_pages(1, 3)
        scraper.send_to_queue()
    else:
        logger.error("Could not establish connection to RabbitMQ. Exiting.")
