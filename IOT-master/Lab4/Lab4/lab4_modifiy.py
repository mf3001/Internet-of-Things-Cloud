

import json,time,csv,sys
import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import aws


table_name = "mta_table_2"


# prompttt
def prompt():
	print ""
	print ">Available Commands are : "
	print "1. plan trip"
	print "2. subscribe to messages"
	print "3. exit"  

def subscribe():
	print "Please enter your phone number:"
	cell_num = raw_input(">>>>")
	client_sns = aws.getClient('sns','us-east-1')
	response = client_sns.subscribe(
		TopicArn='arn:aws:sns:us-east-1:486153037878:mtaSub',
		Protocol='sms',
		Endpoint= cell_num)

def table_scan():
	client_dynamo = aws.getResource('dynamodb','us-east-1')
	global this_table
	this_table = client_dynamo.Table(table_name)
	response1 = this_table.scan(
		FilterExpression = Attr('currentStopId').not_exists()
		)
	return response1


# line_name in the form of [S1, S2, S3]
def get_train_list(line_name):
	print "getting train list..."
	direction = line_name[0]
	line_no = line_name[1]
	train_list = []
	for i in response1['Items']:
		tripId = i['tripId']
		search1 = '_'+line_no
		search2 = '.'+direction
		if tripId.rfind(search1)>0 and tripId.rfind(search2)>0:
			print "find a match"
			print tripId
			train_list.append(i)
	return train_list

def get_incomming_train(target_time, train_list, stopId):
	print "get incomming train..."
	unix_time_max = 2000000000
	incomming_time = unix_time_max
	incomming_item = train_list[0]
	for item in train_list:
		try:
			#print item["futureStops"]
			# print item[0]["futureStops"]
			# print item[1]["futureStops"]
			# print item[2]["futureStops"]
			#print type(item)
			#index = len(item["futureStops"][stopId]) - 1
			train_time = item["futureStops"][stopId]["arrival_time"]
			if train_time > target_time and train_time < incomming_time:
				incomming_time = train_time
				incomming_item = item
		except KeyError:
			pass
	return incomming_item

def get_ETA(destinationStopId, train_item):
	#index = len(train_item["futureStops"][destinationStopId]) - 1
	return train_item["futureStops"][destinationStopId]["arrival_time"]

def plan_trip_now():
	print "planning trip..."
	start_stop_id = "117S"
	transfer_stop_id = "120S"
	destination_stop_id = "127S" #St.42

	#time_at_source = 1456254700
	time_at_source = time.time()

	global response1 
	response1 = table_scan()
	line_1_list = get_train_list('S1')
	line_2_list = get_train_list('S2')
	line_3_list = get_train_list('S3')

	first_train = get_incomming_train(time_at_source, line_1_list, start_stop_id)
	#print first_train["futureStops"]
	#print first_train["futureStops"][transfer_stop_id]
	#print first_train["futureStops"][transfer_stop_id][0]

	#index = len(first_train["futureStops"][transfer_stop_id]) - 1
	time_arriving96 = first_train["futureStops"][transfer_stop_id]["arrival_time"]

	second_train_1 = get_incomming_train(time_arriving96, line_2_list, transfer_stop_id)

	second_train_2 = get_incomming_train(time_arriving96, line_3_list, transfer_stop_id)

	print first_train["tripId"]
	print second_train_1["tripId"]
	print second_train_2["tripId"]

	ETA = min(
		get_ETA(destination_stop_id, first_train),
		get_ETA(destination_stop_id, second_train_1),
		get_ETA(destination_stop_id, second_train_2)
		)
	switch = get_ETA(destination_stop_id, second_train_1) < get_ETA(destination_stop_id, first_train) or get_ETA(destination_stop_id, second_train_2) < get_ETA(destination_stop_id, first_train)
	return (ETA - int(time_at_source)), switch


def main():

	prompt()
	command_str = raw_input(">>>>")
	if command_str == "1":
		time_duration, switch = plan_trip_now()
		print "time_duration and ifswitch:"
		print time_duration
		print switch
		push_content = "Whether to switch?" + str(switch) +"; ETA: "+ str(time_duration/60)+ "mins" 
		client_sns = aws.getClient('sns','us-east-1')
		response = client_sns.publish(
			TopicArn='arn:aws:sns:us-east-1:486153037878:lab4ass1',
			Message='message from edison',
			Subject=push_content,
			MessageStructure='string',
			MessageAttributes={
				'string': {
					'DataType': 'String',
					'StringValue': 'String'
					#'BinaryValue': 'Binary'
				}
			}
		)
	elif command_str == "2":
		subscribe()
	elif command_str == "3":
		pass

	return 0


if __name__ == "__main__":
	main()
	
