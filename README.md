# planeweather
The code for planeweather

## Description
resserver.py has the "main" functionality. It serves the REST queries for flight path
weather.py acts as a rest client and gets the weather data for a given lat,long position. 
geography.py provides the great circle based calculatons. 

### The index.html page
The web server serves static pages from /static/* location. So, /static/index.html is where the browser should be pointed at. 
This web page uses AngularJS. It downloads a list of US airports data. The two dropdown boxes for Origination Airport and Destination airport uses this data. 
When the "Draw Flight Path" button is pressed, the REST GET query parameters are sent to the server. The data is retrieved. It will have the orination, destination and intermediate points as lat,long along with the weather related data at those points. Hovering over the markers will show that information. 

### The REST server
Currently only GET is supported. There is no use case identified for POST, DELETE or other methods. 
it is at /v1/flightdata

The parameters are:
  * sourceAP: The three letter IATA/FAA airport code. For example RDU
  * destAP: The three letter IATA/FAA airport code. For example SFO
  * speed: Average speed of aircraft in kms/hour
  * departure: The departure date and time. For example "2015-02-27T21:20:49.684Z"
  * interval: The intervals in integral hours. This gets weather data for along the path. 

The query data is cached. If the same weather data is requested, it will be retrieved from the cache. 
Note: This is an unmanaged cache. Housekeeping is not provided. 

### Weather data
The weather service is contacted to get weather data for a give location(lat,long). 
http://openweathermap.org/api is used as we can query based on lat,long. 
There are usage limits and we may hit it if used often. 

## Implementation details

### Airport data
This is stored as a static json file. It is fetched from the browser in an AJAX call. Since this has the airport code and lat/long, it is a matter of changing the web form to send the lat/long instead of airport code. 

### Map data
The origination, destination and intermediate points are calculated using the great circle method. 
The points are marked on the map. The intermediate points are calculated based on the distance between orig and dest, the average speed and the requested interval. 
For each of these points, weather data is collected from the weather service. 

This data is sent back to the browser as JSON. 
Note: There is a problem with dynammic JSON data. The same data is captured as a static file and served. This seems to be acceptable. So, for now it only presents static data from RDU to SFO. Anyway, the purpose of demonstrating AJAX call is served. 

# Install Instructions

1. Install the web.py module: sudo easy_install web.py
2. git clone https://github.com/nsrirao/planeweather.git planeweather
3. cd planeweather
4. python restserver.py
5. 
Now, point your brwoser to http://localhost:8080/static/index.html

http://52.11.32.18:8080/static/index.html

