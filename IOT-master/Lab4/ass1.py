import boto3
import mraa
import aws
import math

temp_pin_number=1
temp = mraa.Aio(temp_pin_number)
temperature = float(temp.read())
R = 1023.0/(temperature)-1.0
R = 100000.0*R
temperature=1.0/(math.log(R/100000.0)/4275+1/298.15)-273.15
temperature = str(temperature)


client_sns = aws.getClient('sns','us-east-1');
response = client_sns.publish(
	TopicArn='arn:aws:sns:us-east-1:486153037878:lab4ass1',
	Message='message from edison',
	Subject=temperature,
	MessageStructure='string',
	MessageAttributes={
		'string': {
			'DataType': 'String',
			'StringValue': 'String'
			#'BinaryValue': 'Binary'
		}
	}
)


