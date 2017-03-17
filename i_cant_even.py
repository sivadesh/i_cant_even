import sys
import googlemaps
from datetime import datetime
import urllib2
import json
from yelpapi import YelpAPI
import xml.etree.ElementTree as ET

work_address = sys.argv[1]
travel_distance = sys.argv[2]
restaurants_per_week = sys.argv[3]
bars_per_week = sys.argv[4]
school_importance = sys.argv[5]

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
			# print business['name'] + " " + business['location']['zip_code']
			business_count += 1
	return business_count

def getStateCity(zip_code):
	# Get State and city for given zip code
	gmaps = googlemaps.Client(key='AIzaSyBw6qWv26jGHDDt2Hp0qqck9eLmxB8PxTw')

	geocode = gmaps.geocode(address=zip_code)
	
	state_city = ["","",""]
	for ac in geocode[0]['address_components']:
		if(ac['types'][0] == "administrative_area_level_1"):
			state_city[0] = ac['short_name']
		if(ac['types'][0] == "locality"):
			city = ac['short_name']
			# Replace space with %20 for HTTP URL
			state_city[1] = city.replace(" ", "%20")
		if(ac['types'][0] == "country"):
			state_city[2] = ac['short_name']
	
	return state_city

def getSchoolRating(zip_code):
	# TODO: Change argument to be state, city and only compute unique pairs.
	# Reduces number of calls to getStateCity
	state_city = getStateCity(zip_code)

	if(state_city[2] != 'US'):
		return 0

	#Get ratings for each school district in city
	request_url="http://api.greatschools.org/districts/"+state_city[0]+"/"+state_city[1]+"?key=n80ycnguaxzzb9e0np1qfgxx"
	#print request_url
	response = urllib2.urlopen(request_url)
	root_xml = ET.parse(response).getroot()
	
	ratings=[]
	for district in root_xml:
		district_rating = district.find('districtRating')
		if district_rating is not None:
			ratings.append(int(district_rating.text))
			
	return float(sum(ratings))/len(ratings)


work_zip_code = getWorkZipCode(work_address)

print "Getting all zip codes close to work address"
zip_codes = getAllRadiusZipCodes(work_zip_code, travel_distance)

holy_truth = {}

for zip_code in zip_codes:
	print "Getting number of restarants close to " +zip_code
	restaurants = getNumberOfBusinesses("restaurant", zip_code)
	print zip_code, restaurants
	
	# bars = getNumberOfBusinesses("bar", zip_code)
	
	print "Getting ratings of schools in " +zip_code
	schools = getSchoolRating(zip_code)
	print zip_code, schools

	holy_truth[zip_code] = [restaurants, schools]

# state_city = getStateCity("94043")
# getSchoolRating("94087")

# print holy_truth

ranking = {}
resaturant_weight = float(restaurants_per_week)/14

for zip_code in holy_truth.keys():
	ranking[zip_code] = (resaturant_weight * holy_truth[zip_code][0]) + (float(school_importance) * holy_truth[zip_code][1])

# print ranking
for zip_code in sorted(ranking, key=ranking.get, reverse = True):
	print zip_code, ranking[zip_code]