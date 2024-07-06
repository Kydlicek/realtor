class Listing:
    def __init__(self, data):
        self.hash_id = data['recommendations_data'].get('hash_id', '')
        self.energy_mark = ''
        self.furnished = ''
        self.services_price = ''
        self.add_price_info = ''
        self.last_edit = ''
        self.material = ''
        self.ownership = ''
        self.level = ''
        self.size_m2 = ''
        self.move_in_date = ''

        # Information about Heating, building material etc
        for el in data['items']:
            if el['name'] == 'Aktualizace':
                self.last_edit = el.get('value', '')

            elif el['name'] == 'Stavba':
                self.material = el.get('value', '')

            elif el['name'] == 'Vlastnictví':
                self.ownership = el.get('value', '')

            elif el['name'] == 'Podlaží':
                self.level = el.get('value', '')

            elif el['name'] == 'Užitná plocha':
                self.size_m2 = el.get('value', '')

            elif el['name'] == 'Datum nastěhování':
                self.move_in_date = el.get('value', '')

            elif el['name'] == 'Náklady na bydlení':
                self.services_price = el.get('value', '')

            elif el['name'] == 'Poznámka k ceně':
                self.add_price_info = el.get('value', '')

            elif el['name'] == 'Energetická náročnost budovy':
                self.energy_mark = el.get('value_type', '')

            if data['recommendations_data'].get("energy_efficiency_rating_cb"):
                self.energy_mark = data['recommendations_data'].get("energy_efficiency_rating_cb", '')

            if el['name'] == 'Vybavení':
                self.furnished = el.get('value', '')

        self.prop_info = {
            'last_update': self.last_edit,
            'material': self.material,
            'ownership': self.ownership,
            'prop_level': self.level,
            'size_m2': self.size_m2,
            'energy_mark': self.energy_mark,
            'furnished': self.furnished
        }

        self.seo = data.get('seo', '')
        self.description = data.get('text', {}).get('value', '')
        self.meta_description = data.get('meta_description', '')

        try:
            self.price = {
                'rent': data['price_czk']['value_raw'],
                'deposit': None,
                'services': self.services_price,
                'energy': None,
                'rk': None,
                'add': self.add_price_info
            }
        except KeyError:
            self.price = {
                'rent': None,
                'deposit': None,
                'services': None,
                'energy': None,
                'rk': None,
                'add': None
            }

        address = data.get('locality', {}).get('value', '').split(',')
        city = address[1].split('-') if len(address) > 1 else [address[0], '']
        city_part = city[1].strip() if len(city) > 1 else None

        self.location = {
            'city': city[0].strip(),
            'city_part': city_part,
            'street': address[0] if address else '',
            'gps': {
                'lat': data.get('map', {}).get('lat', None),
                'lon': data.get('map', {}).get('lon', None),
            },
        }

        self.url = f'https://www.sreality.cz/detail/x/x/x/x/{self.hash_id}'
        self.images = [img['_links']['self']['href'] for img in data.get('_embedded', {}).get('images', [])]

        self.renting_details = {
            'rent_date_available': self.move_in_date,
            'rental_period_min': data.get('rental_period_min', None),
            'pets': data.get('pets', None),
            'max_tenants': data.get('max_tenants', None),
            'smoking': data.get('smoking', None),
            'rental_period_max': data.get('rental_period_max', None),
        }

        try:
            self.landlord = {
                'name': data['_embedded']['seller']['user_name'],
                'phone': f'+{data["_embedded"]["seller"]["phones"][0]["code"]} {data["_embedded"]["seller"]["phones"][0]["number"]}',
                'email': data['_embedded']['seller']['_embedded']['premise']['email'],
            }
        except KeyError:
            self.landlord = {'name': None, 'phone': None, 'email': None}

    def get_dict(self):
        return {
            'seo': self.seo,
            'description': self.description,
            'meta_description': self.meta_description,
            'prop_info': self.prop_info,
            'price': self.price,
            'location': self.location,
            'renting_details': self.renting_details,
            'landlord': self.landlord,
            'url': self.url,
            'images': self.images,
        }
