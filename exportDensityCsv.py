import csv
import MySQLdb as mdb
import numpy as np

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runTracks",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT MapMyRunId,StartLat,QuarterLat,HalfLat,ThreeQuarterLat,StartLng,QuarterLng,HalfLng,ThreeQuarterLng from Tracks")
rowsTracks = cur.fetchall()

with open("out.csv", "wb") as csv_file:
    csv_writer = csv.writer(csv_file)
    for row in rowsTracks:
        csv_writer.writerow([str(row['StartLat'])+','+str(row['StartLng'])])
        #csv_writer.writerow([str(row['QuarterLat'])+','+str(row['QuarterLng'])])
        #csv_writer.writerow([str(row['HalfLat'])+','+str(row['HalfLng'])])
        #csv_writer.writerow([str(row['ThreeQuarterLat'])+','+str(row['ThreeQuarterLng'])])