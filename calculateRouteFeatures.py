import pysal
import MySQLdb as mdb
import numpy as np
from scipy import stats

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT MapMyRunId,StartLat,QuarterLat,HalfLat,ThreeQuarterLat,StartLng,QuarterLng,HalfLng,ThreeQuarterLng from Tracks")
rowsTracks = cur.fetchall()
numPoints = 4*len(rowsTracks)
lat = np.zeros(numPoints)
lng = np.zeros(numPoints)

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

latMin = lat.min()
latMax = lat.max()
lngMin = lng.min()
lngMax = lng.max()

X, Y = np.mgrid[latMin:latMax:100j, lngMin:lngMax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([lat, lng])
kernel = stats.gaussian_kde(values)
Z = np.reshape(kernel(positions).T, X.shape)

print latMax

pts = np.random.random((100,2)) #generate some random points
rad = 0.2 #pick an arbitrary radius

#Build a Spatial Weights Matrix
W = pysal.threshold_continuousW_from_array(pts, threshold=rad)
# Note: if your points are in Latitude and Longitude you can increase the accuracy by
#       passing the radius of earth to this function and it will use arc distances.
# W = pysal.threshold_continuousW_from_array(pts, threshold=radius, radius=pysal.cg.RADIUS_EARTH_KM)

print W.weights[0]
#{0: 10, 1: 15, ..... }