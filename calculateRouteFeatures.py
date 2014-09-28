import pysal
import MySQLdb as mdb
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

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

#latMin = lat.min()
#latMax = lat.max()
#lngMin = lng.min()
#lngMax = lng.max()

#X, Y = np.mgrid[latMin:latMax:100j, lngMin:lngMax:100j]
#positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([lat, lng])
kernel = stats.gaussian_kde(values)

n=0
for row in rowsTracks:
	mapMyRunId = row['MapMyRunId']
	startLat = row['StartLat']
	startLng = row['StartLng']
	startDensity = float(kernel([startLat,startLng]))
	quarterLat = row['QuarterLat']
	quarterLng = row['QuarterLng']
	quarterDensity = float(kernel([quarterLat,quarterLng]))
	halfLat = row['HalfLat']
	halfLng = row['HalfLng']
	halfDensity = float(kernel([halfLat,halfLng]))
	threeQuarterLat = row['ThreeQuarterLat']
	threeQuarterLng = row['ThreeQuarterLng']
	threeQuarterDensity = float(kernel([threeQuarterLat,threeQuarterLng]))
	avgDensity = (startDensity+quarterDensity+halfDensity+threeQuarterDensity)/4.0
	cur.execute("UPDATE Tracks SET Popularity=%s WHERE MapMyRunId=%s",(avgDensity,mapMyRunId))
	n = n+1
	print n

con.commit()

cur.close()
con.close()



