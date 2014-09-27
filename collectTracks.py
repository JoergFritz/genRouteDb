from mapmyfitness import MapMyFitness
from googleplaces import GooglePlaces, types
from pandas import Series
import numpy as np
from haversine import haversine
import MySQLdb as mdb
import urllib2
import time

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runTracks",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

# define ways to add info to database
add_track = ("INSERT INTO Tracks "
              "(MapMyRunId, Name, City, Distance, Ascent, Nature, Circularity, \
                StartLat, StartLng, QuarterLat, QuarterLng, HalfLat, HalfLng, \
                ThreeQuarterLat, ThreeQuarterLng, EndLng, EndLat, CenterLat, \
                CenterLng, NumPoints) "
              "VALUES (%(MapMyRunId)s, %(Name)s, %(City)s, %(Distance)s, \
                %(Ascent)s, %(Nature)s, %(Circularity)s, %(StartLat)s, \
                %(StartLng)s, %(QuarterLat)s, %(QuarterLng)s, %(HalfLat)s, \
                %(HalfLng)s, %(ThreeQuarterLat)s, %(ThreeQuarterLng)s, \
                %(EndLat)s, %(EndLng)s, %(CenterLat)s, %(CenterLng)s, %(NumPoints)s)")
add_point = ("INSERT INTO Points "
              "(MapMyRunId, Lat, Lng) "
              "VALUES (%(MapMyRunId)s, %(Lat)s, %(Lng)s)")

# connect to apis
#mmf = MapMyFitness(api_key='4h968vgnddc5r5kswxdpf7tnuat7h8sk', access_token='6cf8fc4094b30b31b49990083c3c25ad3fcfdefc')
mmf = MapMyFitness(api_key='bz2te8jv7g47t39jgq9fgk6frf8u6axb', access_token='5633c4208a61144a285f706f8f8f0c71fbfa499d')
gop = GooglePlaces('AIzaSyBb2jxg7xdMbtQdJNCMgrtrOO6hbb6niEI')

minDist=9637 # start at 3000
maxDist=40000
#maxDist=2050
#stepSize=3000
stepSize=4
filterWords=["walk","bike","cycling","cruiser"]
numKeyPoints=4
keyLat=np.zeros(numKeyPoints)
keyLng=np.zeros(numKeyPoints)
natureDist=np.zeros(numKeyPoints)

# so far Palo Alto, Mountain View, San Francisco, Atherton, Sunnyvale Top, San Carlos
latitude=37.5023724
longitude=-122.2708902

n = 0
curDist=minDist
route_distance=Series()
route_ascent=Series()

# generate list with existing mapMyRunIds to avoid duplication
cur.execute("SELECT Id, MapMyRunId from Tracks")
rowsTracks = cur.fetchall()
existIds = np.zeros(len(rowsTracks), dtype=np.int)
#existIds = np.zeros(len(rowsTracks))
for i in range(len(rowsTracks)):
    existIds[i] = rowsTracks[i]['MapMyRunId']
    #print existIds[i]


while curDist<maxDist:

    try:
        routes_paginator = mmf.route.search(close_to_location=[latitude,longitude], minimum_distance=curDist, maximum_distance=curDist+stepSize, per_page=50)
    except:
        print "json read error in mapmyfitness api request, retrying in 5 seconds"
        time.sleep(5)
        routes_paginator = mmf.route.search(close_to_location=[latitude,longitude], minimum_distance=curDist, maximum_distance=curDist+stepSize, per_page=50)

    page_count = routes_paginator.num_pages  # 2
    page_range = routes_paginator.page_range # [1, 2]
    total_count = routes_paginator.count # 58

    if (total_count<40) or (stepSize<2):
        the_page = routes_paginator.page(1)
        for route in the_page:
            if (route.points() is not None) and (route.points() > 40) and (route.ascent is not None) and (not any(x in route.name for x in filterWords)):
                # get basic route info
                route_id = route.id
                route_distance = route.distance
                route_points = route.points()
                points_count = len(route_points)
                points_range = range(points_count)
                # exclude non-circular routes and routes already in the database
                startPoint = route_points[0]
                endPoint = route_points[points_count-1]
                endDistance = 1000.0*haversine((startPoint['lat'],startPoint['lng']),(endPoint['lat'],endPoint['lng']))
                if (endDistance < route_distance/10.0) and (not route_id in existIds):
                    #print route_id
                    n=n+1 # count this route
                    # get arrays with all points on route
                    pointLat=np.zeros(points_count)
                    pointLng=np.zeros(points_count)
                    for point_num in points_range:
                        point = route_points[point_num]
                        pointLat[point_num] = point['lat']
                        pointLng[point_num] = point['lng']
                        data_point = {
                            'MapMyRunId': route_id,
                            'Lat': pointLat[point_num],
                            'Lng': pointLng[point_num],
                        }
                        cur.execute(add_point, data_point)
                    # find key points to save in tracks database
                    m = 0
                    for point_num in xrange(0,points_count,points_count/4+1):
                        point = route_points[point_num]
                        keyLat[m] = point['lat']
                        keyLng[m] = point['lng']
                        loc = {'lat': keyLat[m], 'lng': keyLng[m]}
                        try:
                            query_result = gop.nearby_search(
                                lat_lng=loc, radius=5000, types=[types.TYPE_PARK,types.TYPE_ZOO], rankby='distance')
                            natureLat = query_result.places[0].geo_location['lat']
                            natureLng = query_result.places[0].geo_location['lng']
                            natureDist[m] = haversine((keyLat[m],keyLng[m]),(natureLat,natureLng))
                        except:
                            print "error caught in google places api request, default value used"
                            time.sleep(1)
                            natureDist[m] = 5000.0
                        m = m+1
                    centerLat = np.mean(keyLat)
                    centerLng = np.mean(keyLng)
                    route_nature = 1.0 - np.mean(natureDist)
                    if route.name is not None:
                        route_name = route.name.encode('ascii', 'ignore')
                    else:
                        route_name = 'None'
                    if route.city is not None:
                        route_city = route.city.encode('ascii', 'ignore')
                    else:
                        route_city = 'None'
                    route_ascent = 1000.0*route.ascent/route.distance
                    sizeLat = 1000*haversine((max(pointLat),np.mean(pointLng)),(min(pointLat),np.mean(pointLng)))
                    sizeLng = 1000*haversine((np.mean(pointLat),max(pointLng)),(np.mean(pointLat),min(pointLng)))
                    route_circularity = 1.0 - abs((sizeLat-sizeLng)/route_distance-1.0/4.0)
                    data_track = {
                        'MapMyRunId': route_id,
                        'Name': route_name,
                        'City': route_city,
                        'Distance': route_distance,
                        'Ascent': route_ascent,
                        'Nature': route_nature,
                        'Circularity': route_circularity,
                        'StartLat': keyLat[0],
                        'StartLng': keyLng[0],
                        'QuarterLat':keyLat[1],
                        'QuarterLng':keyLng[1],
                        'HalfLat': keyLat[2],
                        'HalfLng': keyLng[2],
                        'ThreeQuarterLat': keyLat[3],
                        'ThreeQuarterLng': keyLng[3],
                        'EndLat': endPoint['lat'],
                        'EndLng': endPoint['lng'],
                        'CenterLat': centerLat,
                        'CenterLng': centerLng,
                        'NumPoints': points_count
                    }
                    cur.execute(add_track, data_track)
        curDist=curDist+stepSize
        stepSize=stepSize+1
        print 'Current distance: ' + repr(curDist) + ', tracks added: ' + repr(n)
        # Make sure data is committed to the database
        con.commit()
    else:
        stepSize=stepSize/2

cur.close()
con.close()