import geopy.distance


def calculate_provider_distance(provider_coords,customer_coords):
    dist_in_km = round(geopy.distance.distance(set(provider_coords), customer_coords).km,1)
    return "{0}km".format(dist_in_km)