import geopy.distance
from geopy.geocoders import Nominatim

# import mpu


def calculate_provider_distance(provider_coords,customer_coords):
    print(provider_coords, customer_coords)
    # dist_in_km = round(geopy.distance.vincenty((6.4915007, 3.38217540000005), customer_coords).km,1)
    dist_in_km = round(geopy.distance.vincenty(provider_coords, customer_coords).miles, axis=1)#.km,1)
    # print(mpu.haversine_distance((-6.4915007, 3.38217540000005), (-6.494655799999999, 3.297685499999943)))
    return "{0} miles".format(dist_in_km)


# def get_coords(address):
