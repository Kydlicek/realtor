import requests

# URL for Tableau API endpoint
url = "https://tableau-public.discomap.eea.europa.eu/vizql/w/City_AQ_Viewer_2024/v/EuropeanCityRanking/sessions/F3F7869F1E254E05A354EE07F77C058C-1:2/commands/tabdoc/categorical-filter-by-index"

# Function to filter data for a specific city by index
def get_city_air_quality(city_index):
    # Payload for filtering by city name and fetching air quality data
    payload = {
        "visualIdPresModel": {
            "worksheet": "Cityranking_map",
            "dashboard": "EuropeanCityRanking"
        },
        "globalFieldName": "[federated.1dme4sz0r77tk11fs0j2h0wgg0gj].[none:UA_city_name:nk]",
        "membershipTarget": "filter",
        "filterIndices": [city_index],  # Adjust this index for the city you're targeting
        "filterUpdateType": "filter-replace"
    }

    # Headers, add more if necessary (e.g., session or authentication tokens)
    headers = {
        'Content-Type': 'application/json'
    }

    # Send POST request to the API
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Data retrieved successfully.")
        print(response.text)  # Output the full response for further analysis
    else:
        print(f"Error: {response.status_code} - {response.text}")

# List of cities with their indices (example)
cities = ["Brno", "Český Budějovice", "Hradec Králové", "Praha", "Plzeň"]

# Get air quality data for a specific city by adjusting the index (e.g., 0 for Brno)
city_index = 0  # Brno as an example, adjust index as needed
print(f"Fetching air quality data for: {cities[city_index]}")
get_city_air_quality(city_index)
