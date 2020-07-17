from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="policedata")
location = geolocator.geocode("1601 E IMHOFF RD, NORMAN, OK")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
