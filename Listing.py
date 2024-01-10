class Listing:
    def __init__(self, data):
        #id
        self.listing_id = data['id']
        #property description
        self.description = data['description']
        #pricing
        self.price = {'rent':data['rent'],'deposit':data['deposit'],'services_price':data['services_price'],'energy_price':data['energy_price']}
        #sell 1, rent 2
        self.property_trans_type = data['property_trans_type']
        #flat, house, land, garage, office, commercial, other
        self.property_type = data['property_type']
        #flat, Bedrooms 1, Bathrooms 1, parking 1, size, type 3+kk
        self.rooms = {'bedrooms':data['bedrooms'],'bathrooms':data['bathrooms'],'parking_places':data['parking_places'],'size':data['size'],'kk_size':data['kk_size']}
        #key features
        self.key_features = data['key_features']
        #location
        self.location = {'city':data['city'],'street':data['street'],'street_number':data['street_number'],'zip':data['zip'],'gps':data['gps']}
        self.images = data['images']
        #preference najmu
        self.renting_details = {'rent_date_avaiable': data['rent_date_avaiable'],'furnished':data['furnished'], 'rental_period_min': data['rental_period_min'],'pets':data['pets'],'max_tenants':data['max_tenants'],'smoking':data['smoking'],'rental_period_max':data['rental_period_max'],}
        #landlord
        self.landlord = {'name':data['landlord_name'],'phone':data['landlord_phone'],'email':data['landlord_email']}

        self.time_data = data['time_data']

        self.dic = {self.listing_id,self.description,self.price,self.property_trans_type,self.property_type,self.rooms,self.key_features,self.location,self.images,self.renting_details,self.landlord}
    