BIN_SHEET = "trashbins.csv"
LEVEL_SHEET = "sample_level.csv"
ES_INDICES = ['green', 'yellow', 'red', 'uncertain(green)']
TrashTruckLocation = '40.707240%2C-74.012149';
#'NYSE,%20New%20York,%20NY'

import urllib2
import json
import heapq
from elasticsearch import Elasticsearch



class bin_info(object):
    
    """docstring for bin_info"""
    def __init__(self, bin_csv, level_csv):
        import csv
        super(bin_info, self).__init__()
        self.bin_csv = bin_csv
        self.level_csv = level_csv
        all_bins = {}
        with open(bin_csv, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='|')
            attributes = []
            for idx, line in enumerate(lines):
                #print '[]'.join(line)
                if idx != 0:
                    single_bin = {}
                    for i in xrange(len(line)):
                        single_bin[attributes[i]] = line[i]
                    all_bins[single_bin[attributes[0]]] = single_bin
                else:
                    attributes = line
        self.all_bins = all_bins

        all_alert_bins = {}
        with open(level_csv, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='|')
            attributes = []
            for idx, line in enumerate(lines):
                #print '[]'.join(line)
                if idx != 0:
                    single_bin = {}
                    for i in xrange(6):
                        single_bin[attributes[i]] = line[i]
                    all_alert_bins[single_bin[attributes[0]]] = single_bin
                else:
                    attributes = line
        self.all_alert_bins = all_alert_bins
        #print all_alert_bins['1401728']

    def show_bin(self, bin_id):
        try:
            print self.all_bins[bin_id]
            print self.all_alert_bins[bin_id]
        except:
            pass

    def getBreezo(self,lat, lng):
        target_url = 'http://api.breezometer.com/baqi/?lat=' + lat + '&lon=' + lng + '&key=5d93f7ba935f4deb990a0deca18a65f6'
        response = urllib2.urlopen(target_url)
        jsonResponse = response.read()
        dictResponse = json.loads(jsonResponse)
        #print dictResponse
        #result = {'breezometer_color': dictResponse['breezometer_color'], 
        #'breezometer_aqi': dictResponse['breezometer_aqi'] , 'breezometer_description' }
        return dictResponse

    def generateRoutingURL(self, waypoints):
        target = ''
        counter = 0
        while len(waypoints) != 0 and counter < 23:
            item = heapq.heappop(waypoints)[1]
            itemstr = 'via:'+ str(item['location']['lat']) + '%2C' + str(item['location']['lng'])
            if len(waypoints) != 0 and counter < 23:
                itemstr += '%7C'
            target += itemstr
            counter += 1
        FullURL = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + TrashTruckLocation +'&destination='+ TrashTruckLocation + '&waypoints=' + target + '&key=AIzaSyDvnCt9rVwprcODqeGNoSSyJxbdp9_v69U'
        print "generated google direction API url: " + FullURL
        return FullURL

    def generateRoutingList(self, dictResponse):
        return {"order": dictResponse['routes'][0]["waypoint_order"], "polyline": dictResponse['routes'][0]["overview_polyline"]["points"] }

    def update_response(self):
        es = Elasticsearch()
        result_list = []
        redList = []
        redYellowList = []
        for es_index in ES_INDICES:
            res = es.indices.delete(index= es_index, ignore=[400, 404])
            print res
        for key in self.all_bins:
            value = self.all_bins[key]
            print value
            breezo = self.getBreezo(value['Latitude'], value['Longitude'])
            try:
                #self.all_bins[key]["FullnessLevel"] = "White"
                self.all_bins[key]["FullnessLevel"] = self.all_alert_bins[key]["FullnessLevel"]
                self.all_bins[key]["FullnessAge"] = self.all_alert_bins[key]["FullnessAge"]
                item = {"id": key, 'location':{'lat': value["Latitude"], 'lng': value['Longitude']}, 
                'trashLevel': value['FullnessLevel'], 'airLevel': breezo['breezometer_color'], 
                'airDescription': breezo['breezometer_description'], 'aqi': breezo['breezometer_aqi']}
                if self.all_alert_bins[key]["FullnessLevel"] == 'Red':
                    heapq.heappush(redList,(breezo['breezometer_aqi'], item))
                elif self.all_alert_bins[key]["FullnessLevel"] == 'Yellow':
                    heapq.heappush(redYellowList,(breezo['breezometer_aqi'], item))
            except KeyError:
                self.all_bins[key]["FullnessLevel"] = "Green"
                self.all_bins[key]["FullnessAge"] = "0"
                item = {"id": key, 'location':{'lat': value["Latitude"], 'lng': value['Longitude']}, 
                'trashLevel': value['FullnessLevel'], 'airLevel': breezo['breezometer_color'], 
                'airDescription': breezo['breezometer_description'], 'aqi': breezo['breezometer_aqi']}

            try:
                res = es.index(index = item['trashLevel'].lower(), doc_type = "single_bin_status", id = item['id'], body = json.dumps(item))
            except:
                pass
            print res
        print "Routing now!"
        'https://maps.googleapis.com/maps/api/directions/json?origin=sydney,au&destination=perth,au&waypoints=via:-37.81223%2C144.96254%7Cvia:-34.92788%2C138.60008&key=AIzaSyDvnCt9rVwprcODqeGNoSSyJxbdp9_v69U'
        
        redRouting = urllib2.urlopen(self.generateRoutingURL(redList)).read()
        res = es.index(index = 'redrouting', doc_type = "route", id = 0 , body = redRouting)
        dictRed = json.loads(redRouting)
        redReturnList = self.generateRoutingList(dictRed)
        redList = [redList[i] for i in redReturnList["order"]]
        redReturnJson = json.dumps({'list': redList})
        res = es.index(index = 'redroutinglist', doc_type = "routelist", id = 0 , body = redReturnJson)

        redYellowRouting = urllib2.urlopen(self.generateRoutingURL(redYellowList)).read()
        res = es.index(index = 'redyellowrouting', doc_type = "route", id = 0 , body = redYellowRouting)
        dictRedYellow = json.loads(redYellowRouting)
        redYellowReturnList = self.generateRoutingList(dictRedYellow)
        redYellowList = [redYellowList[i] for i in redYellowReturnList["order"]]
        redYellowReturnJson = json.dumps({'list': redYellowList})
        res = es.index(index = 'redyellowroutinglist', doc_type = "routelist", id = 0 , body = redYellowReturnJson)


        #return result


if __name__ == '__main__':
    test_bins = bin_info(BIN_SHEET, LEVEL_SHEET)
    test_bins.update_response()
    #print test_result['trashList'][0]
    #print test_info.show_bin("1401728")
            