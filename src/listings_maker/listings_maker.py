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
DB_API_URL = os.getenv('DB_API_URL','http://localhost:8000')

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
    try:
        message = json.loads(body)
        logger.info(f"Received message: {message['hash_id']}")
        url = message['url']
        # Scrape the URL
        response = requests.get(url, headers={"user-agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
        message['page_data'] = response.text

        listing = Listing(message).to_dict()
        # Send the processed listing object to the database API's /add endpoint
        db_response = requests.post(f"{DB_API_URL}/add", json=listing)
        db_response.raise_for_status()

        logger.info(f"Successfully processed and stored data for {url}")
        if ch is not None:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 410:
            logger.error(f"Resource gone (410 error) for URL {url}: {e}")
            if ch is not None:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            logger.error(f"Error scraping URL {url}: {e}")
            if ch is not None:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    except requests.RequestException as e:
        logger.error(f"Error scraping URL {url}: {e}")
        if ch is not None:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    except json.JSONDecodeError:
        logger.error("Error decoding message")
        if ch is not None:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if ch is not None:
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

# if __name__ == "__main__":
    # test_message = json.dumps({
    #     'property_type': 'house',
    #     'transaction': 'rent',
    #     'url': 'https://www.sreality.cz/api/cs/v2/estates/997425740',
    #     'hash_id':'997425740'
    # })

    # process_message(None, None, None, test_message)
