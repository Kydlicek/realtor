import pika
import requests
import json
import logging
from models import Listing
import os
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define RabbitMQ settings
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password')
QUEUE_NAME = 'urls_queue'

# Define the database API URL
DB_API_URL = os.getenv('DB_API_URL')
logger.info(DB_API_URL)

def wait_for_rabbitmq_connection(max_retries=10, delay=10):
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

def process_message(ch, method, properties, body):
    """
    Callback function for processing messages from the RabbitMQ queue.
    """
    try:
        message = json.loads(body)
        logger.info(f"Received message: {message}")

        # Extract message fields
        url = message.get("url")

        # Validate URL
        if not url:
            logger.error(f"Invalid message format: {message}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Scrape the URL
        response = requests.get(url, headers={"user-agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
        page_data = response.text

        # Process the page data into a Listing object
        if page_data:
            try:
                listing = Listing(page_data).to_dict()  # Assuming you have a Listing class that parses this data
            except Exception as e:
                logger.error(f"Error converting page data to Listing: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return

        # Prepare payload for database API (you can adjust this as necessary)
        payload = {
            "listing": listing,
            "url": url
        }

        # Send the processed data to the database API
        db_response = requests.post(DB_API_URL, json=payload)
        db_response.raise_for_status()

        logger.info(f"Successfully processed and stored data for {url}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except requests.RequestException as e:
        logger.error(f"Error scraping URL {url}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Requeue message for retry
    except json.JSONDecodeError:
        logger.error("Error decoding message")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge invalid messages
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    """
    Start the RabbitMQ consumer and listen for messages from the queue.
    """
    # Wait for RabbitMQ to be available before starting the consumer
    if not wait_for_rabbitmq_connection():
        logger.error("RabbitMQ connection failed. Exiting.")
        return

    # Use the credentials to connect to RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the queue (make sure it matches the one used by the scraper)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Set up basic consume to listen for messages
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

    logger.info(f"Waiting for messages in {QUEUE_NAME} queue. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
