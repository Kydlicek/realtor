Here’s the updated `README.md` with a section on querying options:

---

# 🏡 Sreality Real Estate Scraper

A Python-based scraper designed to collect real estate listings from a major Czech website. This project includes a FastAPI service to provide access to the scraped data and manage configurations. Built as a microservices-based system, it’s Dockerized for easy deployment, enabling efficient data collection, storage, and processing based on customizable parameters. The architecture is designed for extensibility, allowing users to build additional services or enhance the existing API.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Query Parameters](#api-query-parameters)
- [Error Handling](#error-handling)
- [Future Enhancements](#future-enhancements)

---

## 🔥 Features

- Scrapes real estate listings based on customizable filters
- Stores listing data in MongoDB
- Publishes scraped URLs to RabbitMQ for further processing
- Includes a FastAPI service for data access and configuration management
- Configurable scrape intervals and scraping parameters
- Microservices architecture for easy extensibility with additional features and integrations
- Automatically reconnects to RabbitMQ if the connection is interrupted

---

## 🛠 Tech Stack

- **Docker**: Containerization of the application for easy deployment and scalability
- **FastAPI**: Lightweight web framework for building APIs, used for data access and configuration management
- **RabbitMQ**: Message broker to handle URL publication and manage further processing tasks
- **MongoDB**: NoSQL database for storing the scraped listings in a structured format

---

## 💻 Requirements

- **Docker** and **Docker Compose**
- **Python 3.11+** (if running without Docker)
- MongoDB and RabbitMQ services (can be configured within Docker Compose)

---

## ⚙️ Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/real-estate-scraper.git
   cd real-estate-scraper
   ```

2. **Create a `.env` File**
   Define your environment variables in a `.env` file at the project root. See the [Environment Variables](#environment-variables) section for details.

3. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

---

## 🛠️ Configuration

### Environment Variables

Your `.env` file should include the following configurations:

```dotenv
# MongoDB Parameters
MONGO_URL=mongodb://db:27017
MONGO_DB_CLIENT=main_db

# API Parameters
APP_PORT=8000
DB_API_URL=http://db_api_service:${APP_PORT}

# RabbitMQ Parameters
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=user
RABBITMQ_PASS=password
QUEUE_NAME=urls_queue

# Scraper Parameters
SCRAPE_ALL=true  # Set to true to scrape all property and transaction types

# Property and Transaction Types (used if SCRAPE_ALL is false)
PROPERTY_TYPE=1  # 1 = Flats, 2 = Houses
TRANSACTION_TYPE=2  # 1 = Buy, 2 = Rent

# Additional Settings
SCRAPING_INTERVAL=86400  # Time in seconds between scraping sessions (default: 24 hours)
```

### Key Configurations

- **MONGO_URL**: URL to connect to MongoDB.
- **DB_API_URL**: API endpoint for checking if a listing already exists.
- **RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASS**: Connection details for RabbitMQ.
- **SCRAPE_ALL**: Set to `true` to scrape all properties; otherwise, define specific `PROPERTY_TYPE` and `TRANSACTION_TYPE`.
- **SCRAPING_INTERVAL**: Time interval between scraping sessions in seconds.

---

## 🚀 Running the Project

With Docker Compose:
```bash
docker-compose up --build
```

## 📌 Usage

The scraper can be configured to run continuously in a loop based on `SCRAPING_INTERVAL`. It supports different modes for scraping:

- **Scrape All**: Set `SCRAPE_ALL=true` to scrape all property types and transaction types.
- **Specific Types**: Set `SCRAPE_ALL=false` and use `PROPERTY_TYPE` and `TRANSACTION_TYPE` to filter specific properties.

The scraped data is stored in MongoDB across two collections, organized by property type: **flats** and **houses**. The scraper publishes URLs to RabbitMQ for additional processing, enabling further actions on the collected listings. You can view logs for details on scraped listings and connections.

---

## 🌐 FastAPI Service

This project includes a FastAPI service that provides data access to the scraped listings and allows for configurable settings. Currently, it supports fetching functions but can be customized for other data operations based on user needs. The modular microservices architecture makes it easy to extend the API with additional endpoints or connect other services to enhance functionality.

---

## 🔍 API Query Parameters

The FastAPI service allows querying of the listings database with the following parameters, giving flexibility for targeted searches:

- **`collection_name`** str: The collection to query, such as **flats** or **houses**.
- **`hash_id`** str: A unique identifier for each listing.
- **`id`** str: MongoDB identifier.
- **`transaction`** str: The type of transaction (e.g., buys, rents).
- **`city`** str: Filter listings by city.
- **`price`** int: Set a maximum price for the listings.
- **`size_m2`** int: Specify a minimum size in square meters.
- **`rk`** bool: Boolean to filter based on listings with or without a real estate agent involved.

These parameters enable precise querying, making the API versatile for a variety of applications or custom integrations.

---

## 🔧 Error Handling

The application checks and handles missing or incorrect configurations:

- **Critical Environment Variables**: Logs an error and raises an exception if essential variables (e.g., `RABBITMQ_HOST`, `RABBITMQ_USER`) are missing.
- **Database and API Failures**: Logs any issues in connecting to MongoDB or RabbitMQ, with retries for RabbitMQ connections.
- **Scraping Issues**: Logs any failures during requests, ensuring the application continues even if individual requests fail.

---

## 🔮 Future Enhancements

- **Analytics**: Add performance tracking for the scraper.
- **Enhanced Error Handling**: More specific exception handling and retry mechanisms.
- **Notification System**: Send alerts or notifications for new or specific types of listings.

---

## 📖 License

This project is open-source and available under the [MIT License](LICENSE).

---
