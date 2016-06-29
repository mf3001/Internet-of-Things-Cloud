import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf

import vehicle,alert,tripupdate

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    
    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    with open('./key.txt', 'rb') as keyfile:
        apikey = keyfile.read().rstrip('\n')
        keyfile.close()
 
#FEED_URL = MTA_FEED + APIKEY



    
    VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}    
    alerts = []

    def __init__(self,apikey):
        self.feedurl = self.feedurl + apikey

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        #print type(time)
	try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)
    

        timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)
        tripUpdates = []
	uList = []
        vList = []
    	aList = []
        for entity in feed.entity:
            # Trip update represents a change in timetable
            
            if entity.trip_update and entity.trip_update.trip.trip_id:
                update = tripupdate.tripupdate()
                update.tripId = entity.trip_update.trip.trip_id
                update.routeId = entity.trip_update.trip.route_id
                update.startDate = entity.trip_update.trip.start_date
                tripId = entity.trip_update.trip.trip_id
                
                update.direction = tripId[tripId.rfind('.')+1]# n/s  parse from trip id

                #update.vehicleData = None

                d = OrderedDict()
                for stop in entity.trip_update.stop_time_update:
                    arrivalDict = {}
		    departDict = {}
		    arrive = None
                    depart = None
            
                    arrive = stop.arrival.time
                    depart = stop.departure.time

                    arrivalDict["arrival_time"] = arrive
		    departDict["depart_time"] = depart
		    d[stop.stop_id] = [arrivalDict, departDict]
                update.futureStops = d # Format {stopId : [arrivalTime,departureTime]}
                
                uList.append(update)            
            ##### INSERT TRIPUPDATE CODE HERE ####          

            if entity.vehicle and entity.vehicle.trip.trip_id:
                v = vehicle.vehicle()
                v.currentStopNumber = entity.vehicle.current_stop_sequence
                v.currentStopId = entity.vehicle.stop_id
                v.timestamp = entity.vehicle.timestamp
                v.currentStopStatus = entity.vehicle.current_status
                v.tripId = entity.vehicle.trip.trip_id
                vList.append(v)
            ##### INSERT VEHICLE CODE HERE #####
            if entity.alert:
                a = alert.alert()
        if hasattr(entity.alert, 'trip'):
                    a.tripId = entity.alert.trip.trip_id
                    a.routeId = entity.alert.trip.route_id
                    a.startDate = entity.alert.trip.start_date
                    a.alertMessage = entity.alert.header_text.translation           
            #### INSERT ALERT CODE HERE #####
        
        tripUpdates.append(uList)
        tripUpdates.append(vList)
        tripUpdates.append(aList)
        tripUpdates.append(timestamp)
        return tripUpdates





if __name__ == '__main__':
    up = mtaUpdates('695c5439ae651f2d066964b1b198f7d8')
    print up.getTripUpdates()[3]


