import csv
import MySQLdb as mdb
import numpy as np
import random

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runTracks",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT COUNT('Id') FROM Tracks")
rowsTracks = cur.fetchall()
numTracks = rowsTracks[0]["COUNT('Id')"]
randNums=[0] * 10
for i in range(5):
    randNums[i] = random.randrange(1,numTracks)

cur.execute("SELECT MapMyRunId,CenterLat,CenterLng from Tracks ORDER BY RAND() LIMIT 100000")
rowsTracks = cur.fetchall()

print len(rowsTracks)

with open("out.csv", "wb") as csv_file:
    csv_writer = csv.writer(csv_file)
    for row in rowsTracks:
        csv_writer.writerow([str(row['CenterLat'])+','+str(row['CenterLng'])])
        #csv_writer.writerow([str(row['QuarterLat'])+','+str(row['QuarterLng'])])
        #csv_writer.writerow([str(row['HalfLat'])+','+str(row['HalfLng'])])
        #csv_writer.writerow([str(row['ThreeQuarterLat'])+','+str(row['ThreeQuarterLng'])])