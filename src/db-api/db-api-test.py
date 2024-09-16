import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app, collection  # Import your FastAPI app and MongoDB collection

client = TestClient(app)

# Mock data to simulate MongoDB collection
mock_item = {"_id": "5f63a1a9f1d4c30f1f559d79", "name": "Test Property"}

# Mock ObjectId for bson.objectid.ObjectId usage
from bson.objectid import ObjectId


# Test GET /items
def test_get_items():
    with patch.object(collection, "find", return_value=[mock_item]) as mock_find:
        response = client.get("/items")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1
        mock_find.assert_called_once()  # Ensure that find was called


# Test GET /items/{item_id}
def test_get_item():
    with patch.object(collection, "find_one", return_value=mock_item) as mock_find_one:
        response = client.get(f"/items/{mock_item['_id']}")
        assert response.status_code == 200
        assert response.json()["item"]["name"] == "Test Property"
        mock_find_one.assert_called_once_with({"_id": ObjectId(mock_item["_id"])})


# Test GET /items/{item_id} not found
def test_get_item_not_found():
    with patch.object(collection, "find_one", return_value=None) as mock_find_one:
        response = client.get("/items/invalid_id")
        assert response.status_code == 200
        assert response.json()["error"] == "Item not found"
        mock_find_one.assert_called_once()


# Test POST /items
def test_create_item():
    mock_result = MagicMock(inserted_id="5f63a1a9f1d4c30f1f559d79")
    with patch.object(
        collection, "insert_one", return_value=mock_result
    ) as mock_insert:
        new_item = {"name": "Test Property", "city": "Prague", "budget": "15000"}
        response = client.post("/items", json=new_item)
        assert response.status_code == 200
        assert response.json()["_id"] == str(mock_result.inserted_id)
        mock_insert.assert_called_once_with(new_item)


# Test DELETE /items/{item_id}
def test_delete_item():
    mock_result = MagicMock(deleted_count=1)
    with patch.object(
        collection, "delete_one", return_value=mock_result
    ) as mock_delete:
        response = client.delete(f"/items/{mock_item['_id']}")
        assert response.status_code == 200
        assert response.json()["message"] == "Item deleted"
        mock_delete.assert_called_once_with({"_id": ObjectId(mock_item["_id"])})


# Test DELETE /items/{item_id} not found
def test_delete_item_not_found():
    mock_result = MagicMock(deleted_count=0)
    with patch.object(
        collection, "delete_one", return_value=mock_result
    ) as mock_delete:
        response = client.delete("/items/invalid_id")
        assert response.status_code == 200
        assert response.json()["error"] == "Item not found"
        mock_delete.assert_called_once()
