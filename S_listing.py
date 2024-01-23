class Listing:
    def __init__(self,data):
        self.hash_id = data['recommendations_data']['hash_id']
        self.energy_mark = ''
        self.furnished = ''
        
        #type garage, field building apartment, transaction type: rent, sell, transfer etc, 
        self.seo = data.get('seo', None)
        
        # Property description
        self.description = data['text']['value']
        self.meta_description = data['meta_description']
        
        
        # Pricing
        self.price = {
            'rent': data["price_czk"]['value_raw'],
            'deposit': None,  # Assuming deposit information is not provided
            'services_price': None,  # Assuming services_price information is not provided
            'energy_price': None,  # Assuming energy_price information is not provided
            'rk': None
        }

       # Information about Heating, building material etc
        self.prop_info = data['items']
        for el in self.prop_info:
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
                self.area = el['value']

            #datum nastehovani
            elif el['name'] == 'Datum nastěhování':
                self.move_in_date = el['value']    
            
            #energeticka trida
            elif el['name'] == 'Energetická náročnost budovy':
                self.energy_mark = el['value_type']

            elif data['recommendations_data']["energy_efficiency_rating_cb"]:
                self.energy_mark = data['recommendations_data']["energy_efficiency_rating_cb"]
            
                
            #true == vybaveno, false == nevybaveno
            elif el['name'] == 'Vybavení':
                self.furnished = el['value']


        
        
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
        
        # Images
        self.images = data.get('images', [])

        # Renting details
        self.renting_details = {
            'rent_date_available': self.move_in_date,
            'furnished': self.furnished,
            'rental_period_min': data.get('rental_period_min', None),
            'pets': data.get('pets', None),
            'max_tenants': data.get('max_tenants', None),
            'smoking': data.get('smoking', None),
            'rental_period_max': data.get('rental_period_max', None),
        }

        # Landlord information
        self.landlord = {
            'name': data.get('landlord_name', None),
            'phone': data.get('landlord_phone', None),
            'email': data.get('landlord_email', None),
        }

    def printer(self):
        print(f'description: {self.description[0:30]}')
        print(f'm_description: {self.meta_description}')
        print(self.seo)
        print(self.price)
        print(self.landlord)
        print(self.prop_info)
        print(self.renting_details)
        print(self.last_edit,self.material,self.ownership,self.level,self.area,self.move_in_date, self.furnished,self.energy_mark)