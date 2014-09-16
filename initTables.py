import MySQLdb as mdb
import sys

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")

# create tables
with con:
    cur = con.cursor(mdb.cursors.DictCursor)

    # start new tables if they already exist
    cur.execute("DROP TABLE IF EXISTS Tracks")
    cur.execute("DROP TABLE IF EXISTS Points")
    cur.execute("DROP TABLE IF EXISTS Cities")

    # create Database for summary of running tracks
    cur.execute("CREATE TABLE Tracks \
                (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                MapMyRunId INT, \
                Name VARCHAR(40), \
                City VARCHAR(40), \
                Distance FLOAT, \
                Ascent FLOAT, \
                Nature FLOAT, \
                Offroad FLOAT, \
                Safety FLOAT, \
                PublicTransport FLOAT, \
                View FLOAT, \
                Traffic FLOAT, \
                Popularity FLOAT, \
                Circularity FLOAT, \
                StartLat FLOAT(10,6), \
                StartLng FLOAT(10,6), \
                QuarterLat FLOAT(10,6), \
                QuarterLng FLOAT(10,6), \
                HalfLat FLOAT(10,6), \
                HalfLng FLOAT(10,6), \
                ThreeQuarterLat FLOAT(10,6), \
                ThreeQuarterLng FLOAT(10,6), \
                NumPoints MEDIUMINT) \
                 ")
    cur.execute("CREATE TABLE Points \
                (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                MapMyRunId INT, \
                Lat FLOAT(10,6), \
                Lng FLOAT(10,6)) \
                 ")