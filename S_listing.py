class Listing:
    def __init__(self,data):
        self.hash_id = data['recommendations_data']['hash_id']
        self.energy_mark = ''
        self.furnished = ''
        self.services_price = ''
        self.add_price_info = ''

       # Information about Heating, building material etc
        for el in data['items']:
            if el['name'] == 'Aktualizace':
                self.last_edit=el['value']
            
            elif el['name'] == 'Stavba':
                self.material = el['value']
            
            elif el['name'] == 'Vlastnictví':
                self.ownership = el['value']

            elif el['name'] == 'Podlaží':
                self.level = el['value']

            #uzitna plocha
            elif el['name'] == 'Užitná plocha':
                self.size_m2 = el['value']

            #datum nastehovani
            elif el['name'] == 'Datum nastěhování':
                self.move_in_date = el['value']   

            elif el['name'] == 'Náklady na bydlení':
                self.services_price = el['value'] 
            
            elif el['name'] == 'Poznámka k ceně':
                self.add_price_info = el['value']
            
            #energeticka trida
            elif el['name'] == 'Energetická náročnost budovy':
                self.energy_mark = el['value_type']

            elif data['recommendations_data']["energy_efficiency_rating_cb"]:
                self.energy_mark = data['recommendations_data']["energy_efficiency_rating_cb"]

            #true == vybaveno, false == nevybaveno
            elif el['name'] == 'Vybavení':
                self.furnished = el['value']

        self.prop_info = {
            'last_update':self.last_edit,
            'material': self.material,
            'ownership': self.ownership,
            'prop_level': self.level,
            'size_m2': self.size_m2,
            'energy_mark': self.energy_mark,
            'furnished': self.furnished
        }

        #type garage, field building apartment, transaction type: rent, sell, transfer etc, 
        self.seo = data['seo']
        
        # Property descriptions
        self.description = data['text']['value']
        self.meta_description = data['meta_description']

        # Pricing info
        self.price = {
            'rent': data["price_czk"]['value_raw'],
            'deposit': None,  # Assuming deposit information is not provided
            'services_price': self.services_price ,  # Assuming services_price information is not provided
            'energy_price': None,  # Assuming energy_price information is not provided
            'rk': None,
            'add':self.add_price_info
        }
        
        # Location information
        self.location = {
            'city': None,  # Assuming city information is not provided
            'street': None,  # Assuming street information is not provided
            'street_number': None,  # Assuming street_number information is not provided
            'zip': None,  # Assuming zip information is not provided
            'gps': {
                'lat': data['map']['lat'],
                'lon': data['map']['lon'],
            },
        }

        #external url
        self.url = f'https://www.sreality.cz/detail/x/x/x/x/{self.hash_id}'
        
        #Images
        self.images = []

        for el in data['_embedded']['images']:
            self.images.append(el['_links']['self']['href'])

        # Renting details
        self.renting_details = {
            'rent_date_available': self.move_in_date,
            'rental_period_min': data.get('rental_period_min', None),
            'pets': data.get('pets', None),
            'max_tenants': data.get('max_tenants', None),
            'smoking': data.get('smoking', None),
            'rental_period_max': data.get('rental_period_max', None),
        }

        # Landlord information
        self.landlord = {
            'name': data['_embedded']['seller']['user_name'],
            'phone':f'+{data["_embedded"]["seller"]["phones"][0]["code"]} {data["_embedded"]["seller"]["phones"][0]["number"]}',
            'email': data['_embedded']['seller']['_embedded']['premise']['email'],
        }

    def get_dict(self):
        dic = {
            'seo': self.seo,
            'description':self.description,
            'meta_description': self.meta_description,
            'prop_info': self.prop_info,
            'price':self.price,
            'location':self.location,
            'renting_details':self.renting_details,
            'landlord':self.landlord,
            'url':self.url,
            'images':self.images,
        }
        return dic
 