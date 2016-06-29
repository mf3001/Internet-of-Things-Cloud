import time,csv,sys
from pytz import timezone
from datetime import datetime

sys.path.append('../utils')
import mtaUpdates
import csv

# This script should be run seperately before we start using the application
# Purpose of this script is to gather enough data to build a training model for Amazon machine learning
# Each time you run the script it gathers data from the feed and writes to a file
# You can specify how many iterations you want the code to run. Default is 50
# This program only collects data. Sometimes you get multiple entries for the same tripId. we can timestamp the 
# entry so that when we clean up data we use the latest entry

# Change DAY to the day given in the feed
DAY = datetime.today().strftime("%A")
TIMEZONE = timezone('US/Eastern')

global ITERATIONS

#Default number of iterations
ITERATIONS = 50


#################################################################
####### Note you MAY add more datafields if you see fit #########
#################################################################

# column headers for the csv file
columns =['timestamp','tripId','route','day','timeToReachExpressStation','timeToReachDestination','ifReal2', 'ifReal3']


def main():
    # API key
    ITERATIONS = input("Please input the iterations you want to run (each iteration takes 30 sec)")
    with open('../utils/key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()
	up = mtaUpdates.mtaUpdates(APIKEY)
	line = []
	try:
		with open('rawData4.csv', 'r') as f:
			f.close()
	except:
		with open('rawData4.csv','w') as csvfile:
			f = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			f.writerow(columns)
			csvfile.close()

	with open('rawData4.csv', 'a') as csvfile:
		for i in range(ITERATIONS):
			print "Iteration:" + str(i)
			updateList = up.getTripUpdates()
			for update in updateList:
				if update.direction == "N":
					continue
				if update.tripId[7] != '1' and update.tripId[7] != '2' and update.tripId[7] != '3':
					continue
				#print update.futureStops
				line = []
				now = TIMEZONE.localize(datetime.now())
				last_midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
				time_from_midnight = (now - last_midnight).seconds / 60
				line.append(time_from_midnight)
				line.append(update.tripId)
				if update.tripId[7] == '1':
					line.append('L')
				elif update.tripId[7] == '2' or update.tripId[7] == '3':
					line.append('E')
				line.append(datetime.today().weekday())
				#try:
					#line.append(update.futureStops["117S"][0]["arrivalTime"])
				#except:
					#line.append(None)
				try:
					line.append(update.futureStops["120S"][0]["arrivalTime"])
				except:
					line.append(None)
				try:
					line.append(update.futureStops["127S"][0]["arrivalTime"])
				except:
					line.append(None)
				line.append(False)
				line.append(False)
				#line.append(False)
				if update.vehicleData != None:
					v = update.vehicleData
					if v.currentStopId == "120S":
						line[4] = v.timestamp
						line[6] = True
					if v.currentStopId == "127S":
						line[5] = v.timestamp
						line[7] = True
					#if v.currentStopId == "127S":
						#line[6] = v.timestamp
						#line[9] = True
		
				spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow(line)
			time.sleep(30)
    

if __name__ == '__main__':
	main()
	### INSERT YOUR CODE HERE ###

