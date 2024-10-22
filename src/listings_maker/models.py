from typing import Dict, List, Optional
import re  # Importing regex for city parsing
import json
import requests

class Listing:
    def __init__(self, msg: Dict): 
        data = json.loads(msg['page_data'])
        self.hash_id = str(msg['hash_id'])
        # User and transaction details
        
        self.user_id = None  # ID of the user managing the property
        self.transaction = msg['transaction']
        self.property_type = msg['property_type']

        # GPS coordinates (latitude and longitude only)
        self.gps = self.extract_gps(data)

        # Extract city and city part
        self.city,self.city_part,self.street = self.extract_city_info(data)
        self.size_m2 = self.find_in_items(data,'Užitná ploch')
        self.size_kk = data.get("size_kk", None)

        # Extract price details
        self.price = self.extract_pricing_info(data)

        # Extract additional property details
        self.additional_info = self.extract_additional_info(data)

        # Extract images
        self.images = self.extract_images(data)

        self.description = data.get("description", None)
        self.contact = self.extract_contact_info(data)

        # RK involvement
        self.RK = data.get("RK", False)

        # URL generation
        self.url = f"https://www.sreality.cz/detail/x/x/x/x/{self.hash_id}"

    
    def find_in_items(self,data,name):
        items = data['items']
        for dic in items:
            if dic['name'] == name:
                return (dic['value'])
            
    def extract_gps(self, data: Dict) -> Dict:
        # Extract only the GPS coordinates (latitude and longitude)
        return {
            "lat": data.get("map", {}).get("lat", None),
            "lon": data.get("map", {}).get("lon", None)
        }

    def extract_city_info(self, data):
        full_address = data['locality']['value']
        street = None
        city_name = None
        city_part = None
        
        if full_address:
            # Split the input string by comma to separate street from city
            parts = full_address.split(',')
            
            if len(parts) > 1:
                street = parts[0].strip()  # Extract street
                city_full = parts[1].strip()  # The part containing city info (city and possibly a part)
                
                # Match the city and city part using regex, works for any city
                match = re.match(r"([^\d-]+)\s?(\d+)?", city_full)
                if match:
                    city_name = match.group(1).strip().lower()  # Extracts the city name
                    city_part = match.group(2) if match.group(2) else None  # Extracts city part (if present)
                    city_part = city_part.strip()
                street = str(street).lower()
        return  city_name, city_part, street
    
        

    def extract_pricing_info(self, data: Dict) -> Dict:
        try:
            return {
                "monthly_rent": data["price_czk"]["value_raw"],
                "energy_utilities": data.get("energy_utilities", 0),
                "downpayment": data.get("downpayment", 0),
                "rk_fee": data.get("rk_fee", 0),            # Real estate agent fee
                "currency": "czk",
                "total_first_time": (
                    data["price_czk"]["value_raw"] + 
                    data.get("energy_utilities", 0) + 
                    data.get("downpayment", 0) + 
                    data.get("rk_fee", 0)
                ),
                "recurring_monthly": (
                    data["price_czk"]["value_raw"] + 
                    data.get("energy_utilities", 0)
                )
            }
        except KeyError:
            return {
                "monthly_rent": None,
                "energy_utilities": None,
                "downpayment": None,
                "rk_fee": None,
                "currency": None,
                "total_first_time": None,
                "recurring_monthly": None,
            }

    def extract_additional_info(self, data: Dict) -> Dict:
        try:
            rec_data = data.get('recommendations_data', {})
            additional_info = {
                "floor": self.find_in_items(data, 'Podlaží')[0] if self.find_in_items(data, 'Podlaží') else None,
                "balcony": rec_data.get("balcony", None),
                "cellar": rec_data.get("cellar", None),
                "garden_size_m2": rec_data.get("garden_size_m2", None),
                "garage": rec_data.get("garage", None),
                "bedrooms": rec_data.get("bedrooms", None),
                "furnished": self.find_in_items(data, 'Vybavení') if self.find_in_items(data, 'Vybavení') else None,
                "materials": self.find_in_items(data, 'Stavba') if self.find_in_items(data, 'Stavba') else None,
                "energy_class": self.find_in_items(data, 'Energetická náročnost budovy')[6:7] if len(self.find_in_items(data, 'Energetická náročnost budovy')) >= 7 else None
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
            "hash_id": self.hash_id,                     # Assuming hash_id is used as _id
            "user_id": self.user_id,
            "transaction": self.transaction,
            "property_type": self.property_type,
            "city": self.city,
            "city_part": self.city_part,             # Adding the city_part
            "street": self.street,
            "size_m2": self.size_m2,
            "size_kk": self.size_kk,
            "price": self.price,
            "RK": self.RK,
            "contact": self.contact,
            "additional_info": self.additional_info,
            "description": self.description,
            "photos": self.images,
            "GPS": self.gps,
            "url": self.url
        }
    
    

#this is only for debugging in case everything work fine just comment the code bellow

# url = 'https://www.sreality.cz/api/cs/v2/estates/2293465676'
# response = requests.get(url, headers={"user-agent": "Mozilla/5.0"})
# response.raise_for_status()
# page_data = response.text
# print(Listing(page_data).to_dict())
