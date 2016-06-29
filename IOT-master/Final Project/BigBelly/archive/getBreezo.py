import urllib2
import json

def getBreezo(lat, long):
	response = urllib2.urlopen('https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&key=5d93f7ba935f4deb990a0deca18a65f6')
	jsonResponse = response.read()
	dictResponse = json.loads(jsonResponse)
	# print dictResponse
	return dictResponse["breezometer_aqi"]

if __name__ == '__main__':
	print getBreezo(40.885722, -73.912491)