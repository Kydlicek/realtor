class Listing:
    def __init__(self, data):
        # Listing ID
        self.listing_id = data.get('hash_id', None)

        #type garage, field building apartment, transaction type: rent, sell, transfer etc, 
        self.seo = data.get('seo', None)
        
        # Property description
        self.description = data.get('description', None)
        self.meta_description = data.get('meta_description', None)
        
        # Pricing
        self.price = {
            'rent': data.get('price_summary_czk', None),
            'deposit': None,  # Assuming deposit information is not provided
            'services_price': None,  # Assuming services_price information is not provided
            'energy_price': None,  # Assuming energy_price information is not provided
            'rk': None, # Assuming rk information is not provided
        }
        
        # Rooms information
        self.rooms = {
            'parking_places': None,  # Assuming parking_places information is not provided
            'size': None,  # Assuming size information is not provided
            'kk_size': None,  # Assuming kk_size information is not provided
        }
        # Information about Heating, building material etc
        self.prop_info = None

        # Furniture information
        self.key_features = data.get('furniture', None)
        
        # Location information
        self.location = {
            'city': None,  # Assuming city information is not provided
            'street': None,  # Assuming street information is not provided
            'street_number': None,  # Assuming street_number information is not provided
            'zip': None,  # Assuming zip information is not provided
            'gps': {
                'lat': data.get('locality_gps_lat', None),
                'lon': data.get('locality_gps_lon', None),
            },
        }

        #external url
        self.url = None
        
        # Images
        self.images = data.get('images', [])
        
        # Renting details
        self.renting_details = {
            'rent_date_available': data.get('rent_date_avaiable', None),
            'furnished': data.get('furnished', None),
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

        # dates of creation
        self.time_data = data.get('time_data', None)

        