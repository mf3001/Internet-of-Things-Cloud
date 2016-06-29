import mraa
import time
 
switch_pin_number=8
buzz_pin_number=6
 
# Configuring the switch and buzzer as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)
buzz = mraa.Gpio(buzz_pin_number)
 
# Configuring the switch and buzzer as input & output respectively
switch.dir(mraa.DIR_IN)
buzz.dir(mraa.DIR_OUT)

buzz.write(1)
time.sleep(0.5)
buzz.write(0)

exit
