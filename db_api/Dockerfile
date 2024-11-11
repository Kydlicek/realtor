# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set up the application directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code into the container
COPY . /app

# Run FastAPI when the container starts
CMD uvicorn main:app --host 0.0.0.0 --port ${APP_PORT} --reload
