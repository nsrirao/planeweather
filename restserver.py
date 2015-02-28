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
        sourceAP = p["sourceAP"]
        destAP = p["destAP"]
        speed = float(p["speed"])
        departure = p["departure"]
        interval = float(p["interval"])
        
        if sourceAP == None:
            sourceAP = "RDU"
        
        if destAP == None:
            destAP = "ATL"
            
        if departure == None:
            departure = datetime.now()
        else:
            print departure
        cachekey = (sourceAP, destAP, departure, interval)
        
        if cachekey in flightpaths:
            print "Cache Hit!"
            return json.dumps(flightpaths[cachekey], indent=2)#.replace('\'','"')
        
        point1 = getAirportLatLon(sourceAP)   
        point2 = getAirportLatLon(destAP)
        dis = geography.distance(point1,point2)
        b = geography.bearing(point1, point2)
 
        numIntervals = int((dis*1.0/speed) / interval)

        generaldata = {
        "origin": point1,
        "dest": point2,
        "distance": dis,
        "bearing": b,
        "numintervals": numIntervals,
        "speed": speed,
        }
        weatherdata = []
        weatherdata.append({"gen": generaldata})
        wdict = getWeather( point1[0], point1[1] )
        wdict["point"] = point1
        weatherdata.append(wdict); 
     
        wdict = getWeather( point2[0], point2[1] )
        wdict["point"] = point2
        weatherdata.append(wdict); 

        for x in range(1,numIntervals):
            distancefrompoint1 = speed * x * interval
            pointX = geography.location(point1, distancefrompoint1, b) 
            wdict = getWeather(pointX[0], pointX[1])
            wdict["point"] = pointX
            weatherdata.append(wdict); 

        
        #The data is cached here
        flightpaths[cachekey] = weatherdata
        
        with open('flightdata.json', 'w+') as fp:
            json.dump(flightpaths[cachekey], fp, indent=2)
        return json.dumps(flightpaths[cachekey], indent=2)#.replace('\'','"')
        
        
def getAirportLatLon(apFAA="RDU"):
    """Look up a database of IATA/FAA airport codes.
    return a tuple(latitude,longitude) of that airport
    """
    for record in airports:
        if record["IATAFAA"] == apFAA:
            return (float(record["Latitude"]), float(record["Longitude"]))
           
def getAirports():
        """Takes the csv file of airports data and converts to a dictionary.
        This is invoked once during start so the data is in memory 
        for faster access
        """
        with open("static/airports.dat", "r+") as csvfile:
            fieldnames = ("AirportID",
                            "Name",
                            "City",
                            "Country",
                            "IATAFAA",
                            "ICAO",
                            "Latitude",
                            "Longitude",
                            "Altitude",
                            "Timezone",
                            "DST",
                            "Tz",)
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            a = []
            for record in reader:
                a.append(record)
            return a
        


if __name__ == "__main__":
    flightpaths = {}
    ## Read in the airports data
    airports = getAirports()
    
    #The URLs for accessing the REST services. Since the versioning info 
    #is in the URL, the associated class can be different for other versions
    urls = (
        "/v1/flightdata", "flightdata",
        "/v1/flightdata/", "flightdata",
        "/v1/flightdata/(.*)", "flightdata",
    )

    #Create the web application and run it
    app = web.application(urls, globals())
    app.run()
