# calculate Popularity, Circularity and Offroad scores for newly added routes
import pysal
import MySQLdb as mdb
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from haversine import haversine

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

# get data from databse
cur.execute("SELECT MapMyRunId,StartLat,QuarterLat,HalfLat,ThreeQuarterLat,StartLng,QuarterLng,HalfLng,ThreeQuarterLng,Distance from Tracks")
rowsTracks = cur.fetchall()
numPoints = 4*len(rowsTracks)
lat = np.zeros(numPoints)
lng = np.zeros(numPoints)
cur.execute("SELECT City,Lat,Lng from Cities")
rowsCities = cur.fetchall()

# first loop for calculation of kenel density for popularity
n = 0
for row in rowsTracks:
	mapMyRunId = row['MapMyRunId']
	startLat = row['StartLat']
	lat[n] = startLat
	startLng = row['StartLng']
	lng[n] = startLng
	n = n+1
	quarterLat = row['QuarterLat']
	lat[n] = quarterLat
	quarterLng = row['QuarterLng']
	lng[n] = quarterLng
	n = n+1
	halfLat = row['HalfLat']
	lat[n] = halfLat
	halfLng = row['HalfLng']
	lng[n] = halfLng
	n = n+1
	threeQuarterLat = row['ThreeQuarterLat']
	lat[n] = threeQuarterLat
	threeQuarterLng = row['ThreeQuarterLng']
	lng[n] = threeQuarterLng
	n = n+1
	if (n % 1000) == 0:
	    print n

#latMin = lat.min()
#latMax = lat.max()
#lngMin = lng.min()
#lngMax = lng.max()

#X, Y = np.mgrid[latMin:latMax:100j, lngMin:lngMax:100j]
#positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([lat, lng])
kernel = stats.gaussian_kde(values)

# initialize variables
pointsLat=np.zeros(4)
pointsLng=np.zeros(4)
dist = np.zeros(len(rowsCities))

n=0
for row in rowsTracks:
	mapMyRunId = row['MapMyRunId']
	startLat = row['StartLat']
	startLng = row['StartLng']
	quarterLat = row['QuarterLat']
	quarterLng = row['QuarterLng']
	halfLat = row['HalfLat']
	halfLng = row['HalfLng']
	threeQuarterLat = row['ThreeQuarterLat']
	threeQuarterLng = row['ThreeQuarterLng']
	distance = row['Distance']
	# calculate popularity
	startDensity = float(kernel([startLat,startLng]))
	quarterDensity = float(kernel([quarterLat,quarterLng]))
	halfDensity = float(kernel([halfLat,halfLng]))
	threeQuarterDensity = float(kernel([threeQuarterLat,threeQuarterLng]))
	avgDensity = (startDensity+quarterDensity+halfDensity+threeQuarterDensity)/4.0
	cur.execute("UPDATE Tracks SET Popularity=%s WHERE MapMyRunId=%s",(avgDensity,mapMyRunId))
	# calculate circularity
	pointsLat=[startLat,quarterLat,halfLat,threeQuarterLat]
	pointsLng=[startLng,quarterLng,halfLng,threeQuarterLng]
	# edit here!
	expectedDistance = 0.225*distance # distance between points if they were on circle
	expectedDiameter = 2*0.159*distance
	sizeLat = 1000*haversine((max(pointsLat),np.mean(pointsLng)),(min(pointsLat),np.mean(pointsLng)))
	sizeLng = 1000*haversine((np.mean(pointsLat),max(pointsLng)),(np.mean(pointsLat),min(pointsLng)))
	distQuarter = 1000*haversine((startLat,startLng),(quarterLat,quarterLng))
	distHalf = 1000*haversine((quarterLat,quarterLng),(halfLat,halfLng))
	distThreeQuarter = 1000*haversine((halfLat,halfLng),(threeQuarterLat,threeQuarterLng))
	distStart = 1000*haversine((threeQuarterLat,threeQuarterLng),(startLat,startLng))
	routeCircularity = 1.0 - abs(sizeLat-expectedDiameter)/expectedDiameter - abs(sizeLng-expectedDiameter)/expectedDiameter
	- abs(distQuarter-expectedDistance)/expectedDistance - abs(distHalf-expectedDistance)/expectedDistance
	- abs(distThreeQuarter-expectedDistance)/expectedDistance - abs(distStart-expectedDistance)/expectedDistance
	cur.execute("UPDATE Tracks SET Circularity=%s WHERE MapMyRunId=%s",(routeCircularity,mapMyRunId))
	# calculate simplified off-road metric
	avgLat=(startLat+quarterLat+halfLat+threeQuarterLat)/4
	avgLng=(startLng+quarterLng+halfLng+threeQuarterLng)/4
	for i in range(len(rowsCities)):
	    cityLat = rowsCities[i]['Lat']
	    cityLng = rowsCities[i]['Lng']
	    dist[i] = haversine((cityLat,cityLng),(avgLat,avgLng))
	sortedDistances = np.argsort(dist)[:3]
	offroad = sum(sortedDistances)
	cur.execute("UPDATE Tracks SET Offroad=%s WHERE MapMyRunId=%s",(offroad,mapMyRunId))
	n = n+1
	if (n % 1000) == 0:
	    print n

con.commit()

cur.close()
con.close()



