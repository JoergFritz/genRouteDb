import MySQLdb as mdb
import numpy as np
from haversine import haversine

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT MapMyRunId,City,StartLat,QuarterLat,HalfLat,ThreeQuarterLat,StartLng,QuarterLng,HalfLng,ThreeQuarterLng from Tracks")
rowsTracks = cur.fetchall()
cur.execute("SELECT City,Lat,Lng from Cities")
rowsCities = cur.fetchall()
dist = np.zeros(len(rowsCities))
cityNames=[]
n=0
for row in rowsTracks:
	mapMyRunId = row['MapMyRunId']
	city = row['City']
	startLat = row['StartLat']
	quarterLat = row['QuarterLat']
	halfLat = row['HalfLat']
	threeQuarterLat = row['ThreeQuarterLat']
	startLng = row['StartLng']
	quarterLng = row['QuarterLng']
	halfLng = row['HalfLng']
	threeQuarterLng = row['ThreeQuarterLng']
	avgLat=(startLat+quarterLat+halfLat+threeQuarterLat)/4
	avgLng=(startLng+quarterLng+halfLng+threeQuarterLng)/4
	for i in range(len(rowsCities)):
	    cityNames.append(rowsCities[i]['City'])
	    cityLat = rowsCities[i]['Lat']
	    cityLng = rowsCities[i]['Lng']
	    dist[i] = haversine((cityLat,cityLng),(avgLat,avgLng))
	index_min=dist.argmin()
	closestCity = cityNames[index_min]
	cur.execute("UPDATE Tracks SET City=%s WHERE MapMyRunId=%s",(closestCity,mapMyRunId))
	n = n+1
	print n

con.commit()

cur.close()
con.close()