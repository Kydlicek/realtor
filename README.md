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

Certainly, here’s a streamlined version of the use cases for the `README.md`:

---

## 💡 Use Cases

The Sreality Real Estate Scraper offers versatile applications across the real estate and data analytics sectors:

### 1. **Market Analysis and Trends**
   - Track pricing trends, analyze demand for property types, and monitor market fluctuations over time.

### 2. **Data-Driven Real Estate Investment**
   - Assist investors in identifying profitable properties by analyzing characteristics like price, size, and location.

### 3. **Competitive Analysis for Real Estate Agencies**
   - Enable agencies to monitor competitor listings, pricing strategies, and market positioning.

### 4. **Automated Alerts for Potential Buyers**
   - Set up notifications for buyers based on custom criteria, such as price range, location, or property type.

### 5. **Property Valuation and Price Prediction Models**
   - Develop predictive models to estimate property values using historical and real-time listing data.

### 6. **Data Enrichment for Real Estate Websites**
   - Enrich property listings with additional insights, like neighborhood pricing trends or market comparisons.

### 7. **Research and Academic Studies**
   - Provide a robust dataset for research on real estate trends, socioeconomic impacts on property prices, and urban development.

---

These use cases showcase the broad applicability of the Sreality Real Estate Scraper for real estate professionals, data analysts, and researchers alike.

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

The FastAPI service allows querying of the listings database with the following parameters, offering flexibility for targeted searches.

- **Collection Name**: Specify either **flats** or **houses** based on the property type you wish to search.

- **API Endpoint**: Most likely `http://0.0.0.0:8000/{collection_name}`, if the default configuration has not been modified.

**Parameters**:

- **`hash_id`** *(str)*: A unique identifier for each listing.
- **`id`** *(str)*: MongoDB identifier.
- **`transaction`** *(str)*: Type of transaction (e.g., "buy" or "rent").
- **`city`** *(str)*: Filter listings by city name.
- **`price`** *(int)*: Maximum price for the listings.
- **`size_m2`** *(int)*: Minimum size in square meters.
- **`rk`** *(bool)*: Filter listings based on the presence or absence of a real estate agent.

These parameters enable precise querying, making the API versatile for a variety of applications or custom integrations.

---

## 🔧 Error Handling

The application checks and handles missing or incorrect configurations:

- **Critical Environment Variables**: Logs an error and raises an exception if essential variables (e.g., `RABBITMQ_HOST`, `RABBITMQ_USER`) are missing.
- **Database and API Failures**: Logs any issues in connecting to MongoDB or RabbitMQ, with retries for RabbitMQ connections.
- **Scraping Issues**: Logs any failures during requests, ensuring the application continues even if individual requests fail.

---

## 🆕 Upcoming Features and Improvements

This project is continuously evolving, with planned enhancements focused on improving data quality, usability, and extensibility. Here’s a look at some of the upcoming features and improvements:

### 1. **Enhanced Data Cleaning and Validation**
   - **Improved Data Consistency**: Implementing advanced cleaning rules to standardize property data, ensuring consistent formatting across all fields (e.g., uniform city names, standardized price and size formats).
   - **Automatic Error Detection**: Identifying and handling common data issues like incomplete or duplicate listings, reducing noise in the dataset.
   - **Customizable Cleaning Pipelines**: Allowing users to configure data cleaning steps based on their needs, enhancing flexibility for different applications.

### 2. **Extended Filtering and Search Options**
   - **Additional Query Parameters**: Adding more filters to refine search results, such as property age, building materials, and energy efficiency ratings.
   - **Dynamic Range Filtering**: Enabling range-based filtering for fields like `price` and `size_m2`, allowing users to specify minimum and maximum values.

### 3. **Data Enrichment and Analytics**
   - **Automated Data Enrichment**: Integrating additional sources to enrich listings with data like neighborhood amenities, historical pricing trends, and estimated property value.
   - **Analytics and Reporting**: Adding basic analytics to summarize listings, identify trends, and visualize data distributions (e.g., price distribution by city).

### 4. **Notification and Alert System**
   - **User-Defined Notifications**: Allowing users to set alerts for new listings that match specific criteria, making it easier to stay updated on relevant properties.
   - **Scheduled Summaries**: Generating periodic summaries of new or notable listings to keep users informed.

---

## 📖 License

This project is open-source and available under the [MIT License](LICENSE).

---


