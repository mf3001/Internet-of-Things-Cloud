import mraa
import time
import pyupm_i2clcd as lcd
import math
from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import Context
from myblog import models as m
 
switch_pin_number=8
temp_pin_number=1
myLcd = lcd.Jhd1313m1(1, 0x3E, 0x62)
 
# Configuring the switch and buzzer as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)
temp = mraa.Aio(temp_pin_number)

# Configuring the switch and buzzer as input & output respectively
switch.dir(mraa.DIR_IN)

print "Press Ctrl+C to escape..."
try:
	while (1):
		if (switch.read()):     # check if switch pressed
			temperature = float(temp.read())
			R = 1023.0/(temperature)-1.0
			R = 100000.0*R
			temperature=1.0/(math.log(R/100000.0)/4275+1/298.15)-273.15
			myLcd.setCursor(1,0)
			myLcd.write('Temperature ')
			myLcd.write(str(temperature))
except KeyboardInterrupt:
	exit
 
