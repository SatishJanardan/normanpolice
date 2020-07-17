from pprint import pprint
#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter
import requests, datetime, time
import pyowm
from police.models import Crime, Case
import googlemaps


APIKEY = 'AIzaSyCjoD7pepMRf4kU5ubWvpAMO_2os3VLAK8' #google maps apikey
CLIENTID = '502544939589-difhk70em8dlbvmd5q9rgfg7e4jrfqkc.apps.googleusercontent.com'
CLIENTSECRET = 'fcHxu2RjAzvTNEDZcFXuH5-S'
GOOGLEURL = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=' + APIKEY
#geolocator = Nominatim(user_agent="normanpolicegps")
#geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)
maxtries = 10000

class Test(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)


gmaps = googlemaps.Client(key=APIKEY)

# Geocoding an address
#location = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')


count=0
for crime in Crime.objects.filter():
	#crime = Crime.objects.get(incpk)
	#print(crime)
	if crime.crimeLat == 35.221770 and crime.crimeLong == -97.444960 and count < maxtries:  # if lat,long has defaults check if can get updated values
		address = crime.crimeLocation
		address = address + ', NORMAN, OK'
		count+=1
		try:
			location = gmaps.geocode(address)

			crime.crimeLat = location[0]["geometry"]['location']['lat']
			crime.crimeLong = location[0]["geometry"]['location']['lng']
			if count % 50 == 0: 
				print(crime.id,address)
			crime.save()
			#time.sleep(2)
		except:
			print(count,"incident location does not exist-->",address)


for case in Case.objects.filter():
	#crime = Crime.objects.get(incpk)
	#print(crime)
	if case.caseLat == 35.221770 and case.caseLong == -97.4449600 and count < maxtries:  # if lat,long has defaults check if can get updated values
		address = case.caseLocation
		address = address + ', NORMAN, OK'
		count+=1
		try:
			location = gmaps.geocode(address)

			case.caseLat = location[0]["geometry"]['location']['lat']
			case.caseLong = location[0]["geometry"]['location']['lng']
			if count % 50 == 0: 
				print(case.id.address)
			case.save()
			#time.sleep(2)
		except:
			print(count,"case location does not exist-->",address)


locerror = json.load(location)

#location = geolocator.geocode("1601 E IMHOFF RD, NORMAN, OK")
#print(location.address)
#print((location.latitude, location.longitude))
#print(location.raw)
'''
APIKEY = 'ec7ffc0bc2580e24e3d239c27b7da9ab'
lat=location.latitude
lon=location.longitude
time=datetime.datetime(2020,6, 1, 0, 0).timestamp()
print(time)
req = 'https://api.openweathermap.org/data/2.5/timemachine?lat={' + str(lat) + '}&lon={' + str(lon) + '}&dt={' + str(time) + '}&appid={' + APIKEY + '}'
print(req)
r = requests.get(req)
pprint(r.json())

owm = pyowm.OWM('ec7ffc0bc2580e24e3d239c27b7da9ab') # TODO: Replace <api_key> with your API key
mgr = owm.weather_manager()
print(owm)
weather = mgr.weather_at_place('1601 E IMHOFF RD, NORMAN, OK')  # get the weather now
dump_dict = weather.to_dict()
print(dump_dict)


place = owm.weather_at_place('NORMAN, US')
weather = place.get_weather()
print(weather.get_sunrise_time(timeformat='iso')) # Prints time in GMT timezone
print(weather.get_sunset_time(timeformat='iso')) # Prints time in GMT timezone


APIKEY = 'ec7ffc0bc2580e24e3d239c27b7da9ab'
lat=location.latitude
lon=location.longitude
time=datetime.datetime(2020,6, 1, 0, 0).timestamp()
print(time)
req = 'https://api.openweathermap.org/data/2.5/timemachine?lat={' + str(lat) + '}&lon={' + str(lon) + '}&dt={' + str(time) + '}&appid={' + APIKEY + '}'
r = requests.get(req)
pprint(r.json())
'''
