import requests

# Define the API URL
url = "http://localhost:8000/rents"

# Set the query parameters
params = {
    "id": "671694fba4e3e7a9ad1fe560",  # Your MongoDB ObjectId
}

# Make the GET request to FastAPI
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Retrieve the properties as JSON
    properties = response.json()
    
    # Open a text file and write the results
    with open('result.txt', 'w') as file:
        file.write("Retrieved properties:\n")
        file.write(str(properties))  # Convert the JSON to a string and write to the file
    
    print("Results saved to result.txt")
else:
    print(f"Error: {response.status_code}")
