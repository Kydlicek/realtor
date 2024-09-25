from typing import Dict, List, Optional


class Listing:
    def __init__(self, data: Dict):
        self.hash_id = data['recommendations_data'].get('hash_id', '')

        # Extract various property info
        self.prop_info = self.extract_property_info(data)

        # Extract price details
        self.price = self.extract_pricing_info(data)

        # Extract location details
        self.location = self.extract_location_info(data)

        # Extract images
        self.images = self.extract_images(data)

        # SEO and Description
        self.seo = data.get('seo', '')
        self.description = data.get('text', {}).get('value', '')
        self.meta_description = data.get('meta_description', '')

        # Renting details
        self.renting_details = self.extract_renting_details(data)

        # Landlord details with error handling
        self.landlord = self.extract_landlord_info(data)

        # Neighborhood and contact info (from updated JSON)
        self.neighborhood = data.get('neighborhood', {})
        self.contact = data.get('contact', {})

        # Pricing details from the updated JSON structure
        self.pricing_details = data.get('pricing_details', {})

        # URL generation
        self.url = f'https://www.sreality.cz/detail/x/x/x/x/{self.hash_id}'

    def extract_property_info(self, data: Dict) -> Dict:
        prop_info = {
            'last_update': '',
            'material': '',
            'ownership': '',
            'prop_level': '',
            'size_m2': '',
            'energy_mark': '',
            'furnished': ''
        }

        # Process the items for property info
        for el in data.get('items', []):
            if el['name'] == 'Aktualizace':
                prop_info['last_update'] = el.get('value', '')

            elif el['name'] == 'Stavba':
                prop_info['material'] = el.get('value', '')

            elif el['name'] == 'Vlastnictví':
                prop_info['ownership'] = el.get('value', '')

            elif el['name'] == 'Podlaží':
                prop_info['prop_level'] = el.get('value', '')

            elif el['name'] == 'Užitná plocha':
                prop_info['size_m2'] = el.get('value', '')

            elif el['name'] == 'Energetická náročnost budovy':
                prop_info['energy_mark'] = el.get('value_type', '')

            elif el['name'] == 'Vybavení':
                prop_info['furnished'] = el.get('value', '')

        # Override energy mark if present in recommendations_data
        if data['recommendations_data'].get("energy_efficiency_rating_cb"):
            prop_info['energy_mark'] = data['recommendations_data'].get("energy_efficiency_rating_cb", '')

        return prop_info

    def extract_pricing_info(self, data: Dict) -> Dict:
        # Safely extract price data with defaults
        try:
            return {
                'rent': data['price_czk']['value_raw'],
                'deposit': None,
                'services': data.get('services_price', ''),
                'energy': None,
                'rk': None,
                'add': data.get('add_price_info', '')
            }
        except KeyError:
            return {
                'rent': None,
                'deposit': None,
                'services': None,
                'energy': None,
                'rk': None,
                'add': None
            }

    def extract_location_info(self, data: Dict) -> Dict:
        address = data.get('locality', {}).get('value', '').split(',')
        city = address[1].split('-') if len(address) > 1 else [address[0], '']
        city_part = city[1].strip() if len(city) > 1 else None

        return {
            'city': city[0].strip(),
            'city_part': city_part,
            'street': address[0] if address else '',
            'gps': {
                'lat': data.get('map', {}).get('lat', None),
                'lon': data.get('map', {}).get('lon', None),
            },
        }

    def extract_images(self, data: Dict) -> List[str]:
        # Extract image URLs from the data
        return [img['_links']['self']['href'] for img in data.get('_embedded', {}).get('images', [])]

    def extract_renting_details(self, data: Dict) -> Dict:
        # Extract renting details with fallbacks
        return {
            'rent_date_available': data.get('move_in_date', ''),
            'rental_period_min': data.get('rental_period_min', None),
            'pets': data.get('pets', None),
            'max_tenants': data.get('max_tenants', None),
            'smoking': data.get('smoking', None),
            'rental_period_max': data.get('rental_period_max', None),
        }

    def extract_landlord_info(self, data: Dict) -> Dict:
        # Handle errors when extracting landlord information
        try:
            return {
                'name': data['_embedded']['seller']['user_name'],
                'phone': f'+{data["_embedded"]["seller"]["phones"][0]["code"]} {data["_embedded"]["seller"]["phones"][0]["number"]}',
                'email': data['_embedded']['seller']['_embedded']['premise']['email'],
            }
        except (KeyError, IndexError, TypeError):
            return {'name': None, 'phone': None, 'email': None}
