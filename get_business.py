from yelpapi import YelpAPI

yelp_api = YelpAPI('Icci0UP1WX7R0wrGfLEYCw', 'lWMwaew0FlWFRZVXZIqIKjIhYneiPkFiIWioqk1YsdLkVgbRUGhgS9velfSGoioT')

search_results = yelp_api.search_query(term='restaurants', location='98104', sort_by='rating', limit=50)

for result in search_results['businesses']:
   print result['name'] + " " +str(result['location']['zip_code'])