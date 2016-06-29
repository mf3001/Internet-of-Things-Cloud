import sys
import csv

file1 = open('rawData.csv', 'rb')
file2 = open('rawDataNew.csv', 'wb')

reader = csv.reader(file1)
writer = csv.writer(file2)

for row in reader:
   row.remove(row[4])
   writer.writerow(row)
