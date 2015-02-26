#!/usr/bin/env python
import web
import json
from pprint import pprint
from urlparse import parse_qsl
import csv
import geography
from weather import getWeather


class flightdata:        
    def GET(self):
        p = parse_qsl(web.ctx.query[1:])
        p = dict(p)
        print web.ctx.fullpath
        ## Form data from the GET URL
        sourceAP = p['sourceAP']
        destAP = p['destAP']
        speed = float(p['speed'])
        departure = p['departure']
        interval = float(p['interval'])
        
        if sourceAP == None:
            sourceAP = 'RDU'
        
        if destAP == None:
            destAP = 'ATL'
            
        if departure == None:
            departure = datetime.now()
        else:
            departure = None ###### !!!!!!!!!!!!!!!!!!!!!!!!!
        cachekey = (sourceAP, destAP, departure, interval)
        
        if cachekey in flightpaths:
            return flightpaths[cachekey]
        
        point1 = getAirportLatLon(sourceAP)
        point2 = getAirportLatLon(destAP)
        dis = geography.distance(point1,point2)
        b = geography.bearing(point1, point2)
 
        numIntervals = int((dis*1.0/speed) / interval)
                
        weatherdata = {}
        weatherdata[point1] = getWeather( point1[0], point1[1] )
        weatherdata[point2] = getWeather( point2[0], point2[1] )

        for x in range(1,numIntervals):
            distancefrompoint1 = speed * x * interval
            pointX = geography.location(point1, distancefrompoint1, b) 
            weatherdata[pointX] = getWeather(pointX[0], pointX[1])
        flightpaths[cachekey] = weatherdata
        return flightpaths[cachekey]
        
        
def getAirportLatLon(apFAA='RDU'):
    '''Look up a database of airport codes.
    return a tuple(latitude,longitude)
    '''
    for record in airports:
        if record['IATAFAA'] == apFAA:
            return (float(record['Latitude']), float(record['Longitude']))
           
def getAirports():
        '''Takes the csv file of airports data and converts to a dictionary.
        '''
        with open('static/airports.dat', 'r+') as csvfile:
            fieldnames = ('AirportID',
                            'Name',
                            'City',
                            'Country',
                            'IATAFAA',
                            'ICAO',
                            'Latitude',
                            'Longitude',
                            'Altitude',
                            'Timezone',
                            'DST',
                            'Tz',)
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            a = []
            for record in reader:
                a.append(record)
            return a
        


if __name__ == "__main__":
    flightpaths = {}
    ## Read in the airports data
    airports = getAirports()
    urls = (
        '/v1/flightdata', 'flightdata',
        '/v1/flightdata/', 'flightdata',
        '/v1/flightdata/(.*)', 'flightdata',
    )

    app = web.application(urls, globals())
    app.run()