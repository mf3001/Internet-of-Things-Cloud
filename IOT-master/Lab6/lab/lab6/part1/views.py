from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers

import mraa
import time
import pyupm_i2clcd as lcd
import math
# Create your views here.


def get_temp(request):
    temp_pin_number=1
    temp = mraa.Aio(temp_pin_number)
    temperature = float(temp.read())
    R = 1023.0/(temperature)-1.0
    R = 100000.0*R
    temperature=1.0/(math.log(R/100000.0)/4275+1/298.15)-273.15
    d = {'temperature': temperature}
    print(d)
    return JsonResponse(d)

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    template = loader.get_template('part1/index.html')
    #print "view.index requested"
    return HttpResponse(template.render(request))