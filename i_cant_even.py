import sys
import googlemaps
from datetime import datetime
import urllib2
import json
from yelpapi import YelpAPI

work_address = sys.argv[1]
travel_distance = sys.argv[2]
restaurants_per_week = sys.argv[3]
bars_per_week = sys.argv[4]

def getWorkZipCode(work_address):
	gmaps = googlemaps.Client(key='AIzaSyBw6qWv26jGHDDt2Hp0qqck9eLmxB8PxTw')

	# Request directions via public transit
	# now = datetime.now()
	# distance_result = gmaps.distance_matrix("1301 2nd Ave Seattle, WA",
	#                                         "2105 5th Ave Seattle, WA",
	#                                          mode="transit",
	#                                          departure_time=now,
	#                                          units="imperial")

	# print distance_result['rows'][0]['elements'][0]['distance']['text'] + " " + distance_result['rows'][0]['elements'][0]['duration']['text']

	# Get User's Work Zip Code
	geocode = gmaps.geocode(address=work_address)

	for ac in geocode[0]['address_components']:
		if(ac['types'][0] == "postal_code"):
			#print ac['short_name']
			work_zip_code=ac['short_name']

	return work_zip_code

def getAllRadiusZipCodes(work_zip_code, travel_distance):
	# Get all zip codes in a radius of Travel Distance
	request_url="https://www.zipcodeapi.com/rest/WKiZcyx6wskyBfJ4VLc08HpurGBqSBXPmgPyPmFlP0UrfEvbpIcypC3QiEhbgf1C/radius.json/"+work_zip_code+"/"+travel_distance+"/miles?minimal"
	response = urllib2.urlopen(request_url)
	response_json = json.load(response)
	print response_json['zip_codes']
	return response_json['zip_codes']

def getNumberOfBusinesses(business_type, zip_code):
	# Get number of businesses per zip code
	yelp_api = YelpAPI('Icci0UP1WX7R0wrGfLEYCw', 'lWMwaew0FlWFRZVXZIqIKjIhYneiPkFiIWioqk1YsdLkVgbRUGhgS9velfSGoioT')

	business_count = 0
	search_results = yelp_api.search_query(term=business_type, location=zip_code, limit = 50)
	# print str(zip_code) + " " +str(search_results['total'])
	for business in search_results['businesses']:
		if(business['location']['zip_code'] == zip_code):
			#print business['name'] + " " + business['location']['zip_code']
			business_count += 1
	return business_count


work_zip_code = getWorkZipCode(work_address)
zip_codes = getAllRadiusZipCodes(work_zip_code,travel_distance)
restaurants = {}
for zip_code in zip_codes:
	restaurant_count = getNumberOfBusinesses("restaurant", zip_code)
	restaurants[zip_code] = restaurant_count
	#bars = getNumberOfBusinesses("bar", zip_code)

print restaurants