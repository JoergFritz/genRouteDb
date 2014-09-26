import pysal
import MySQLdb as mdb
import numpy as np

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT MapMyRunId,StartLat,QuarterLat,HalfLat,ThreeQuarterLat,StartLng,QuarterLng,HalfLng,ThreeQuarterLng from Tracks")
rowsTracks = cur.fetchall()

pts = np.random.random((100,2)) #generate some random points
rad = 0.2 #pick an arbitrary radius

#Build a Spatial Weights Matrix
W = pysal.threshold_continuousW_from_array(pts, threshold=rad)
# Note: if your points are in Latitude and Longitude you can increase the accuracy by
#       passing the radius of earth to this function and it will use arc distances.
# W = pysal.threshold_continuousW_from_array(pts, threshold=radius, radius=pysal.cg.RADIUS_EARTH_KM)

print W.weights[0]
#{0: 10, 1: 15, ..... }