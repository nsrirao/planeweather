# Background

The expected weather conditions along the planned route of a plane are essential for a pilot.
As a pilot I would like to have a web application that gives me this forecast at a requested granularity. 


# Problem Definition
Given a source, a destination and a time of departure create a weather forecast report for the journey. 

## Inputs
*  Source [as Latitude / Longitude or Airport Code]
*  Destination 
*  Time of Departure
*  Average Speed
*  Time Interval (in hours)

## Outputs
Create a weather forecast report once every "Time Interval" 
The report should include Temperature, humidity, wind speed and other information of note.


## Weather
Weather data can be obtained from any source on the internet.

http://weathersource.com/weather-api has a good API and a free account. 

## Solution
Implement the backend of this solution in python (or another language of your choice) and host the code on github.
The application should be hosted on ec2 (heroku or others) and provide login credentials. 

## Solution Details
*  Backend should be written as a stand alone RESTFul service that the UI can use
*  Compute a route between the source and the destination using straight line, great circle on any algorithm of your choice.
*  WebUI should show a map with source, destination and the route.
   (google maps API, or similar)
*  WebUI should be created as a single page javascript app.
*  Weather forecast data should be rendered in any suitable format.
*  Weather data should be cached. 

## Extra
* It should be possible to provide a departure time in the past.

## Evaluation
* We are looking for a complete and deployable solution.
* Write tests.
* Write a README if necessary.
* Commit often to the repository.
* We encourage you to ask questions and make assumptions explicit.  
