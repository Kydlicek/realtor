Here's a comprehensive `README.md` for your scraper project, incorporating all the configurations and setup instructions:

---

# 🏡 Sreality Real Estate Scraper

A FastAPI-based scraper designed to collect real estate listings from a major Czech website. This project is Dockerized for easy deployment, allowing you to collect, store, and process data on properties based on customizable parameters.

---

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Future Enhancements](#future-enhancements)

---

## 🔥 Features

- Scrapes real estate listings based on customizable filters
- Stores listing data in MongoDB
- Publishes scraped URLs to RabbitMQ for further processing
- Configurable scrape intervals and scraping parameters
- Automatically reconnects to RabbitMQ if the connection is interrupted

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

Without Docker:
1. Ensure MongoDB and RabbitMQ are running.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}
   ```

---

## 📌 Usage

The scraper can be configured to run continuously in a loop based on `SCRAPING_INTERVAL`. It supports different modes for scraping:

- **Scrape All**: Set `SCRAPE_ALL=true` to scrape all property types and transaction types.
- **Specific Types**: Set `SCRAPE_ALL=false` and use `PROPERTY_TYPE` and `TRANSACTION_TYPE` to filter specific properties.

The scraped data is stored in MongoDB and sent to RabbitMQ for additional processing. You can view logs for details on scraped listings and connections.

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

Let me know if you need additional information or have any questions!
