from typing import Dict, List, Optional
import re  # Importing regex for city parsing
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Listing:
    def __init__(self, msg: Dict):
        data = json.loads(msg["page_data"])
        self.hash_id = str(msg["hash_id"])
        # User and transaction details

        self.transaction = msg["transaction"]
        self.property_type = msg["property_type"]

        # GPS coordinates (latitude and longitude only)
        self.gps = self.extract_gps(data)

        # Extract the number of rooms in the property
        self.description = self.get_description(data)
        self.meta_description = self.get_meta_descripton(data)

        # Extract city and city part
        self.city, self.city_part, self.street = self.extract_location(data)
        self.size_m2 = str(self.find_in_items(data, "Užitná ploch"))
        self.size_kk = self.get_kk_size()

        # Extract price details
        self.price = self.extract_pricing_info(data)

        # Extract additional property details
        self.additional_info = self.extract_additional_info(data)

        # Extract images
        self.images = self.extract_images(data)

        self.contact = self.extract_contact_info(data)
        # RK involvement
        self.rk = self.get_rk(data)

        # URL generation
        self.url = f"https://www.sreality.cz/detail/x/x/x/x/{self.hash_id}"

    def get_kk_size(self):
        if self.property_type == "flats":
            # Regular expression pattern to match the format "2+kk"
            pattern = r"\b\d+\+\w+\b"

            match = re.search(pattern, self.meta_description)
            if match:
                return match.group()
            else:
                return None
        else:
            return None

    def get_description(self, data):
        # Check if "text" exists in the dictionary and has the "value" field
        if "text" in data and "value" in data["text"]:
            return data["text"]["value"]
        else:
            return None

    def get_meta_descripton(self, data):
        try:
            return data["meta_description"]
        except:
            return None

    def get_rk(self, data):
        try:
            l = data["_embedded"]["seller"]
            return True
        except:
            return False

    def find_in_items(self, data, name):
        items = data["items"]
        for dic in items:
            if dic["name"] == name:
                return dic["value"]

    def extract_gps(self, data: Dict) -> Dict:
        # Extract only the GPS coordinates (latitude and longitude)
        return {
            "lat": data.get("map", {}).get("lat", None),
            "lon": data.get("map", {}).get("lon", None),
        }

    def extract_location(self, data):
        location = {"street": None, "city": None, "city_part": None}

        # Check if "locality" and "value" exist in the dictionary
        if "locality" in data and "value" in data["locality"]:
            value = data["locality"]["value"]

            # Pattern to match "Street, City - City Part" format
            city_part_pattern = r"(.+?),\s*(.+?)\s*-\s*(.+)"
            # Pattern to match "Street, City" format without city part
            city_pattern = r"(.+?),\s*(.+)"

            # Attempt to match with city part
            match = re.match(city_part_pattern, value)
            if match:
                location["street"] = match.group(1).strip()
                location["city"] = match.group(2).strip()
                location["city_part"] = match.group(3).strip()
            else:
                # Attempt to match without city part
                match = re.match(city_pattern, value)
                if match:
                    location["street"] = match.group(1).strip()
                    location["city"] = match.group(2).strip()

        return location["city"], location["city_part"], location["street"]

    def extract_pricing_info(self, data: Dict) -> Dict:
        try:
            return str(data["price_czk"]["value_raw"])
            # preparatiom for more coplex pricing

            # "energy_utilities": data.get("energy_utilities", 0),
            # "downpayment": data.get("downpayment", 0),
            # "rk_fee": data.get("rk_fee", 0),
            # "currency": "czk",
            # "total_first_time": (
            #     data["price_czk"]["value_raw"]
            #     + data.get("energy_utilities", 0)
            #     + data.get("downpayment", 0)
            #     + data.get("rk_fee", 0)
            # ),
            # "recurring_monthly": (
            #     data["price_czk"]["value_raw"] + data.get("energy_utilities", 0)
            # ),

        except KeyError:
            # return {
            #     "monthly_rent": None,
            #     "energy_utilities": None,
            #     "downpayment": None,
            #     "rk_fee": None,
            #     "currency": None,
            #     "total_first_time": None,
            #     "recurring_monthly": None,
            # }
            return None

    def extract_additional_info(self, data: Dict) -> Dict:
        try:
            rec_data = data.get("recommendations_data", {})
            additional_info = {
                "floor": (
                    self.find_in_items(data, "Podlaží")[0]
                    if self.find_in_items(data, "Podlaží")
                    else None
                ),
                "balcony": rec_data.get("balcony", None),
                "cellar": rec_data.get("cellar", None),
                "garage": rec_data.get("garage", None),
                "bedrooms": rec_data.get("bedrooms", None),
                "furnished": (
                    self.find_in_items(data, "Vybavení")
                    if self.find_in_items(data, "Vybavení")
                    else None
                ),
                "materials": (
                    self.find_in_items(data, "Stavba")
                    if self.find_in_items(data, "Stavba")
                    else None
                ),
                "energy_class": (
                    self.find_in_items(data, "Energetická náročnost budovy")[6:7]
                    if len(self.find_in_items(data, "Energetická náročnost budovy"))
                    >= 7
                    else None
                ),
            }
            return additional_info
        except Exception as e:
            pass

    def extract_images(self, data: Dict) -> List[str]:
        # Extract image URLs from the data
        return [
            img["_links"]["self"]["href"]
            for img in data.get("_embedded", {}).get("images", [])
        ]

    def extract_contact_info(self, data: Dict) -> Dict:
        try:
            return {
                "name": data["_embedded"]["seller"]["user_name"],
                "email": data["_embedded"]["seller"]["_embedded"]["premise"]["email"],
                "phone": f'+{data["_embedded"]["seller"]["phones"][0]["code"]} {data["_embedded"]["seller"]["phones"][0]["number"]}',
            }
        except (KeyError, IndexError, TypeError):
            return {"name": None, "phone": None, "email": None}

    def to_dict(self) -> Dict:
        # Return all the attributes of the instance as a dictionary matching your MongoDB schema
        return {
            "hash_id": self.hash_id,
            "transaction": self.transaction,
            "property_type": self.property_type,
            "city": self.city,
            "city_part": self.city_part,
            "street": self.street,
            "size_m2": self.size_m2,
            "size_kk": self.size_kk,
            "price": self.price,
            "rk": self.rk,
            "contact": self.contact,
            "gps": self.gps,
            "url": self.url,
            "additional_info": self.additional_info,
            "description": self.description,
            "meta_description": self.meta_description,
            "photos": self.images,
        }
