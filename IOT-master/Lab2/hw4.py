import mraa
import time
import pyupm_i2clcd as lcd
import math
import boto
from boto import kinesis
import json
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from datetime import datetime
t = str(datetime.now())

###############################################################################
ACCOUNT_ID = '486153037878'
IDENTITY_POOL_ID = 'us-east-1:343fd9ae-5dbb-4a98-994d-d0a0fd0cfee1'
ROLE_ARN = 'arn:aws:iam::486153037878:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])
###############################################################################

switch_pin_number=8
temp_pin_number=1
myLcd = lcd.Jhd1313m1(1, 0x3E, 0x62)

# Configuring the switch and buzzer as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)
temp = mraa.Aio(temp_pin_number)

# Configuring the switch and buzzer as input & output respectively
switch.dir(mraa.DIR_IN)

client_kinesis = boto.connect_kinesis( 
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

#kinesis = client_kinesis.create_stream("IOT",1)
stream_list = client_kinesis.list_streams
# for i in range(20):
#     client_kinesis.put_record("IOT","20","20")




this_table = Table('temperature', connection=client_dynamo )

stream = True
num = 0
print "Press Ctrl+C to escape..."
try:
    	while (1):
                if (switch.read()):     # check if switch pressed
                        temperature = float(temp.read())
                        R = 1023.0/(temperature)-1.0
                        R = 100000.0*R
                        temperature=1.0/(math.log(R/100000.0)/4275+1/298.15)-273.15
			temperature = str(temperature)
                        if (stream is True):
                                stream = not stream
                                myLcd.setCursor(1,0)
                                myLcd.write('Kinesis ')
                                client_kinesis.put_record("IOT_temperature",temperature,' ')


                        elif (stream is False):
                                stream = not stream
                                myLcd.setCursor(1,0)
                                myLcd.write('DynamoDB')
                                this_table.put_item(data={'No.': num, 'Temperature': temperature, 'Time': t })
                                num+=1
			time.sleep(0.3)
                        
except KeyboardInterrupt:
        exit

