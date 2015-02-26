import math
from math import radians, cos, sin, asin, sqrt, degrees, atan2

EarthRadius = 6371.009 #Mean radius in kilometers
''' Formulae from: http://www.movable-type.co.uk/scripts/latlong.html '''

def distance(point1,point2,miles=False):
    '''Calculate the distance on the greater circle between 2 points 
    given their latitude and longitudes. 
    Returns the distance in Kilometers.
    '''
    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    
    a = list( map(math.radians, [lat1, lng1, lat2, lng2]) )
    lat1, lng1, lat2, lng2 = a
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    #Apply the haversine formula
    a = pow(sin(dlat/2.0),2) + (cos(lat1)*cos(lat2)*pow(sin(dlng/2.0),2))
    c = 2 * math.atan2(sqrt(a), sqrt(1-a))
    d = EarthRadius * c

    if miles:
        return d / 1.60934
    else:
        return d



def bearing(point1,point2,initial=True):
    ''' Get the bearing (direction) to head out given the 2 points.
    point1: Source point (latitude,longitude) as a tuple. 
    point2: Destination point(latitude,longitude) as a tuple. 
    initial: True (default): Initial bearing at Source
             False: Bearing at destination
    returns: bearing in degrees
    '''
    
    # unpack lattude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2
    if ( initial ):
        pass
    else:
        lat1, lng1 = point2
        lat2, lng2 = point1


    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = list(map(radians, [lat1, lng1, lat2, lng2]))
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    y = sin(dlng) * cos(lat2)
    x = cos(lat1)*sin(lat2) - (sin(lat1)*cos(lat2)*cos(dlng))
    bearing = atan2(y,x)
    return (degrees(bearing)+360) % 360
    
    
def location(point1, distance, bearing):
    ''' Determine the latitude and longitude of a point "distance" kms away
    on the greater circle from point1 starting with a given bearing.
    point1: tuple (latitude,longitude)
    distance: in kilometers
    bearing: The direction starting at point1 in degrees
    
    Returns (latitude,longitude) as a tuple
    '''
    
    lat1, lng1 = point1
    lat1, lng1, = list(map(radians, [lat1, lng1]))

    d = distance / EarthRadius
    t = radians(bearing)
    
    lat2 = asin ( sin(lat1)*cos(d) +
                  cos(lat1)*sin(d)*cos(t) )
                
    lng2 = lng1 + atan2( sin(t)*sin(d)*cos(lat1),
                         cos(d)-sin(lat1)*sin(lat2) )
    
    lng2 = (lng2+3*math.pi)%(2*math.pi) - math.pi
    
    lat2, lng2, = list(map(degrees, [lat2, lng2]))
    
    return (lat2,lng2)
    


