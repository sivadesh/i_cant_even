import xml.etree.ElementTree as ET
import urllib2

request_url="http://api.greatschools.org/districts/CA/sunnyvale?key=n80ycnguaxzzb9e0np1qfgxx"
response = urllib2.urlopen(request_url)
root_xml = ET.parse(response).getroot()
for district in root_xml:
	district_rating = district.find('districtRating')
	if district_rating is not None:
		print grandchild.text