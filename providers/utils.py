from rest_framework.validators import ValidationError


def validate_coords(coords):
    lat = float(coords.split(',')[0])
    lng = float(coords.split(',')[1])
    if not (lat >= -90 and lat <= 90) or not (lng >= -90 and lng <= 90):
        raise ValidationError('invalid cordinates. coords should be in range of -90 to 90')
    return coords