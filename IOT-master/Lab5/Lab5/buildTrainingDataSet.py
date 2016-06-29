## This program is used to clean out the data from the csv that you collected.
## It aims at removing duplicate entries and extracting any further insights 
## that the author(s) of the code may see fit

## Usage (for file as is currently): python buildTrainingDataSet.py <filename of file from part 1>
  
import sys
import csv
# Pandas is a python library used for data analysis
import pandas as pd
from pandas import read_csv
from pytz import timezone
from datetime import datetime


TIMEZONE = timezone('America/New_York')


def main(fileHandle):
	# This creates a dataframe
	rawData = read_csv(fileHandle)
	# Remove duplicate entries based on tripId, retain the one with maximum timestamp
	data = rawData.groupby('tripId').apply(lambda x: x.ix[x.timestamp.idxmax()])
	# Drop the nan values for 42 and 96
	data = data.dropna()
	# Seperate all the local trains and form a new data frame
	localTrains = data[data.route == 'L']
	# Express trains
	expressTrains = data[data.route == 'E']
	# 1. Find the time difference (to reach 96th) between all combinations of local trains and express
	# 2. Consider only positive delta
	# 3. Make the final table
	#['timestamp','tripId','route','day','timeToReachSource(116)','timeToReachExpressStation(96)',
	#'timeToReachDestination(42)', 'ifReal1', 'ifReal2', 'ifReal3']
	# Create a new data frame for final table
	col_list = ['tripId','starttime','day','level','time1at96','travelTimeLocal','travelTimeExpress','switch']
	finalData = pd.DataFrame([],columns=col_list)

	for index,train_local in localTrains.iterrows():
		time1at96 = train_local['timeToReachExpressStation']
		time1at42 = train_local['timeToReachDestination']
		starttime = int(train_local['tripId'][:6])/100
		travelTimeLocal = time1at42 - time1at96
		level = int(train_local['ifReal2']) + int(train_local['ifReal3'])
		#print int(localTrains.ifReal1)+int(localTrains.ifReal2)+int(localTrains.ifReal3)
		for index,train_express in expressTrains.iterrows():
			if train_express['timeToReachExpressStation'] > time1at96 :
				travelTimeExpress = train_express['timeToReachDestination'] - time1at96
				if travelTimeExpress < travelTimeLocal:
					switch = 1
				else:
					switch = 0
				col = [train_local.tripId,starttime,train_local.day,level,time1at96,travelTimeLocal,travelTimeExpress,switch]
				temp_data = pd.DataFrame([col],columns=col_list)
				finalData = finalData.append(temp_data)
				#finalData.to_csv("finalData.csv",index=False)
				break
	finalData.to_csv("finalData4.csv",index=False)
		


if __name__ == "__main__":

	lengthArg = len(sys.argv)


	if lengthArg < 2:
		print "Missing arguments"
		sys.exit(-1)

	if lengthArg > 2:
		print "Extra arguments"
		sys.exit(-1)
	
	fileHandle = sys.argv[1]
	main(fileHandle)
