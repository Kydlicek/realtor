import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient
from main import app  # Import your FastAPI app from your db_api code
import mongomock
from unittest.mock import patch

# Create a test client for FastAPI
client = TestClient(app)

# Mock MongoDB connection
@pytest.fixture(autouse=True)
def mock_mongo():
    with patch("main.MongoClient", return_value=mongomock.MongoClient()) as mock_client:
        yield mock_client


# Test POST /{collection_name} to save data to the database
def test_save_to_db():
    # Mock data
    collection_name = "test_collection"
    data = {"name": "Test Property", "address": "123 Test Ave", "price": "1000"}

    # Send a POST request
    response = client.post(f"/{collection_name}", json=data)
    
    # Check if the response has a 200 status code
    assert response.status_code == 200
    
    # Check the response format
    assert "_id" in response.json()


# Test GET /{collection_name}/{item_id} to retrieve an item by its ID
def test_get_item():
    # Insert an item into the test collection
    collection_name = "test_collection"
    data = {"name": "Test Property", "address": "123 Test Ave", "price": "1000"}

    # Insert the item using the API
    post_response = client.post(f"/{collection_name}", json=data)
    inserted_id = post_response.json()["_id"]

    # Retrieve the item using the GET request
    response = client.get(f"/{collection_name}/{inserted_id}")

    # Check if the response has a 200 status code
    assert response.status_code == 200

    # Validate the response data
    item = response.json()["item"]
    assert item["name"] == "Test Property"
    assert item["address"] == "123 Test Ave"
    assert item["price"] == "1000"


# Test DELETE /{collection_name}/{item_id} to delete an item by its ID
def test_delete_item():
    # Insert an item into the test collection
    collection_name = "test_collection"
    data = {"name": "Test Property", "address": "123 Test Ave", "price": "1000"}

    # Insert the item using the API
    post_response = client.post(f"/{collection_name}", json=data)
    inserted_id = post_response.json()["_id"]

    # Delete the item
    response = client.delete(f"/{collection_name}/{inserted_id}")

    # Check if the response has a 200 status code
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}

    # Verify that the item no longer exists
    get_response = client.get(f"/{collection_name}/{inserted_id}")
    assert get_response.status_code == 404


# Test PUT /{collection_name}/{item_id}/status to update item status
def test_update_item_status():
    # Insert an item into the test collection
    collection_name = "test_collection"
    data = {"name": "Test Property", "address": "123 Test Ave", "price": "1000"}

    # Insert the item using the API
    post_response = client.post(f"/{collection_name}", json=data)
    inserted_id = post_response.json()["_id"]

    # Update the status of the item
    response = client.put(f"/{collection_name}/{inserted_id}/status", json={"new_status": "sold"})

    # Check if the response has a 200 status code
    assert response.status_code == 200
    assert response.json() == {"message": f"Item {inserted_id} status updated"}

    # Verify the status update
    get_response = client.get(f"/{collection_name}/{inserted_id}")
    assert get_response.status_code == 200
    assert get_response.json()["item"]["status"] == "sold"
