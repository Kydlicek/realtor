# Use official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define environment variables (if needed)
ENV RABBITMQ_HOST=localhost

# Run the consumer when the container starts
CMD ["python", "listings_maker.py"]
