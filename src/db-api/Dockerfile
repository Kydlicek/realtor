# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set up the application directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code into the container
COPY . /app

# Expose FastAPI port (8000)
EXPOSE 8000

# Run FastAPI when the container starts
CMD uvicorn main:app --host 0.0.0.0 --port 5000
