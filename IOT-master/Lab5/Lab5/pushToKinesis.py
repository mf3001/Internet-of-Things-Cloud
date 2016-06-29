
# This program sends the data to kinesis. You do not need to modify this code except the Kinesis stream name.
# Usage python pushToKinesis.py <file name>
# a lambda function will be triggered as a result, that will send it to AWS ML for classification
# Usage python pushToKinesis.py <csv file name with extension>
import urllib2,contextlib
import google.protobuf
import sys,csv,json

import boto3

sys.path.append('../utils')
import aws
import mtaUpdates   
from pytz import timezone
from datetime import datetime
import gtfs_realtime_pb2

KINESIS_STREAM_NAME = 'IOT5'


def main(fileName):
    
    # connect to kinesis
    with open('../utils/key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()
        feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
        feedurl = feedurl + APIKEY



        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)
        row=[]
        nearest = 0
        #nearest_tripId =''
        for entity in feed.entity:
            if entity.vehicle and entity.vehicle.trip.trip_id and entity.vehicle.stop_id:
                vehicleData = entity.vehicle
                tripId = vehicleData.trip.trip_id
                stopId = vehicleData.stop_id
                if (tripId[7] == '1') and (stopId[3] == 'S') and (int(str(stopId)[0:3]) <= 117) and (int(str(stopId)[0:3]) > nearest):
                    nearest = int(stopId[0:3])
                    nearest_tripId = tripId
                    push = int(str(nearest_tripId)[0:6])/100
        row.append(push)
        row.append(datetime.today().weekday())
        with open(fileName, 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(row)
                    


	kinesis = aws.getClient('kinesis','us-east-1')
	data = [] # list of dictionaries will be sent to kinesis
	with open(fileName,'rb') as f:
		dataReader = csv.DictReader(f)
		for row in dataReader:
        #print row
			kinesis.put_record(StreamName=KINESIS_STREAM_NAME, Data=json.dumps(row), PartitionKey='0')
			break

		f.close()






if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Missing arguments"
        sys.exit(-1)
    if len(sys.argv) > 2:
        print "Extra arguments"
        sys.exit(-1)
    try:
        fileName = sys.argv[1]
        main(fileName)
    except Exception as e:
        raise e
