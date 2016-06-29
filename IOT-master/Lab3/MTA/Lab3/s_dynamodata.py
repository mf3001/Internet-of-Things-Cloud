# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python dynamodata.py
# *********************************************************************************************
import json,time,sys
from collections import OrderedDict
import threading
from threading import Thread
# import boto
# import boto.dynamodb2
# from boto.dynamodb2.table import Table
# from boto.dynamodb2.fields import HashKey, RangeKey
import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws 





table_name = 'mta_table_3'


def initial_table():
	client_dynamo = aws.getResource('dynamodb','us-east-1')
	try:
		this_table = client_dynamo.create_table(
			TableName = table_name,
			KeySchema=[
				{
					'AttributeName': 'tripId',
					'KeyType': 'HASH'
				}
			],
			AttributeDefinitions=[
				{	'AttributeName': 'tripId',
					'AttributeType': 'S'
				}
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}
		)
		print "table created"
	except:
		this_table = client_dynamo.Table(table_name)
		print 'using existing table'
	return this_table

def item_in_table(this_item, timestamp):
	global this_table
	result = 1
	try:
		response = this_table.get_item(Key = {'tripId' : this_item.tripId, 'timestamp' : timestamp})
	except:
		result = 0
	return result

def add_item_u(this_item, timestamp):
	this_table.put_item(
			Item = {
				 	'tripId': this_item.tripId,
				 	'routeId': this_item.routeId ,
				 	'startDate': this_item.startDate,
				 	'direction': this_item.direction,
				 	'futureStopData': this_item.futureStops,
				 	'timestamp': timestamp
			})

def add_item_v(this_item, timestamp):
	this_table.put_item(
			Item = {
				 	'tripId': this_item.tripId,
				 	'currentStopNumber': this_item.currentStopNumber,
				 	'currentStopId': this_item.currentStopId,
				 	'timestamp_v': this_item.timestamp,
				 	'currentStopStatus': this_item.currentStopStatus,
				 	'timestamp': timestamp
			})

def update_item_u(this_item, timestamp):

	this_table.update_item(
	Key={
	'tripId': this_item.tripId,
	'timestamp': timestamp
	},
	UpdateExpression='SET routeId = :val1,startDate = :val2,direction = :val3,futureStops = :val4',
	ExpressionAttributeValues={
				':val1': this_item.routeId,
				':val2': this_item.startDate,
				':val3': this_item.direction,
				':val4': this_item.futureStops,
		}
	)

def update_item_v(this_item, timestamp):

	this_table.update_item(
		Key={
				'tripId': this_item.tripId,
				'timestamp': timestamp
		},
		UpdateExpression='SET currentStopNumber = :val1 ,  currentStopId = :val2, timestamp_v = :val3,   currentStopStatus = :val4',
		ExpressionAttributeValues={
				':val1': this_item.currentStopNumber,
				':val2': this_item.currentStopId,
				':val3': this_item.timestamp,
				':val4': this_item.currentStopStatus,
		}
	)


def update_data():
	while (1):
		print "update_data"
		global this_table
		info = mtaUpdates.mtaUpdates('695c5439ae651f2d066964b1b198f7d8')
		data=info.getTripUpdates()

		all_items = this_table.scan()["Items"]


	with this_table.batch_writer() as batch:
		batch.put_item(
			Item={
				'account_type': 'standard_user',
				'username': 'johndoe',
				'first_name': 'John',
				'last_name': 'Doe',
				'age': 25,
				'address': {
					'road': '1 Jefferson Street',
					'city': 'Los Angeles',
					'state': 'CA',
					'zipcode': 90001
				}
			}
		)


	# repeat this every 30 sec
		timestamp = data[3]
		i = 0
		for j in xrange(0,len(data[i])):
			this_item = data[i][j]
			if item_in_table(this_item,timestamp):
				update_item_u(this_item,timestamp)
			else:
				add_item_u(this_item,timestamp)

		i = 1
		for j in xrange(0,len(data[i])):
			this_item = data[i][j]
			if item_in_table(this_item, timestamp):
				update_item_v(this_item,timestamp)
			else:
				add_item_v(this_item,timestamp)

def clean_data():
	while (1):
		pass
		print "clean_data"
		global this_table
		timeNow = int(time.time())
		timeDiff = timeNow - 120
		response = this_table.scan(
			FilterExpression = Attr('timestamp').lt(timeDiff)
			)
		for i in response['Items']:
			tripId = i['tripId']
			timestamp = i['timestamp']
			this_table.delete_item(
				Key = {
					'tripId': tripId,
					'timestamp': timestamp
					},
				)
		time.sleep(60)



if __name__ == '__main__':
	this_table = initial_table()
	t1 = Thread(target=update_data)
	t1.daemon = True
	t1.start()
	t2 = Thread(target=clean_data)
	t2.daemon = True
	t2.start()
	do_exit = False
	while do_exit == False:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt: 
			do_exit = True
	#threading.Timer(3,update_data).start()
	#threading.Timer(3,clean_data).start()
















