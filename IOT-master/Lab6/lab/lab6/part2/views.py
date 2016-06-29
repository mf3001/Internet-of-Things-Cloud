from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
from pprint import pprint
import requests
import pyowm
#import urlparse
from part2.models import City

owm = pyowm.OWM('12acaab40f90242b4ebc27b42c1e488f')
location = {
'Boston': {'lat':42.36,'lng': -71.05}, 
'Philadelphia': {'lat': 39.95, 'lng':-75.17},
'NewYork': {'lat':40.71,'lng': -74.01}, 
'Washington': {'lat':38.53,'lng': -77.02}, 
}

# def route_plan(request, source, destination):
#      # s_return = requests.get('http://api.openweathermap.org/data/2.5/weather?q='
#      #    + source 
#      #    + '&APPID=12acaab40f90242b4ebc27b42c1e488f')
#      # d_return = requests.get('http://api.openweathermap.org/data/2.5/weather?q='
#      #    + destination 
#      #    + '&APPID=12acaab40f90242b4ebc27b42c1e488f')
#     location = {'Boston': {'lat':42.36,'lng': -71.05}, 'Philadelphia': {'lat': 39.95, 'lng':-75.17}}
#     s_observation = owm.weather_at_place(source)
#     s_temp = s_observation.get_weather().get_temperature('celsius')['temp']
#     d_observation = owm.weather_at_place(destination)
#     d_temp = d_observation.get_weather().get_temperature('celsius')['temp']
#     s_return = {'temp': s_temp, 'location': location[source]}
#     d_return = {'temp': d_temp, 'location': location[destination]}
#     return_dict = {'source': s_return, 'destination': d_return}
#     print "in function route_plan"
#     print source
#     print destination
#     print return_dict

#     return JsonResponse(return_dict)




def index(request):
    q_dict =  request.GET
    if q_dict:
        source = q_dict['source']
        destination = q_dict['destination']

        s_observation = owm.weather_at_place(source)
        s_temp = s_observation.get_weather().get_temperature('celsius')['temp']
        d_observation = owm.weather_at_place(destination)
        d_temp = d_observation.get_weather().get_temperature('celsius')['temp']
        
	new_entry = City(city=source, latitude=location[source]['lat'], longitude=location[source]['lng'], temperature=s_temp)
	new_entry.save()
	s_entry = City.objects.get(city=source)
	s_return = {'temp': s_temp, 'location': {'lat':float(s_entry.latitude), 'lng':float(s_entry.longitude)}}
        d_entry = City.objects.get(city=destination)
	d_return = {'temp': d_temp, 'location': {'lat':float(d_entry.latitude), 'lng':float(d_entry.longitude)}}
        return_dict = {'source': s_return, 'destination': d_return}
        print return_dict
        return JsonResponse(return_dict)
    else:
        #return HttpResponse("Hello, world. You're at the polls index.")
        template = loader.get_template('part2/index.html')
        #print "view.index requested"
        return HttpResponse(template.render(request))

