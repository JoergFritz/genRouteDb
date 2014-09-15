import MySQLdb as mdb
import sys

# import user defined stuff
from dbFunctions import checkTableExists

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")

# create tables
with con:
    cur = con.cursor(mdb.cursors.DictCursor)

    # start new tables if they already exist
    if checkTableExists(con,"Tracks"):
        cur.execute("DROP TABLE IF EXISTS Tracks")
    if checkTableExists(con,"Points"):
        cur.execute("DROP TABLE IF EXISTS Points")
    if checkTableExists(con,"Cities"):
        cur.execute("DROP TABLE IF EXISTS Cities")

    # more simple version
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
                StartLat FLOAT, \
                StartLng FLOAT, \
                QuarterLat FLOAT, \
                QuarterLng FLOAT, \
                HalfLat FLOAT, \
                HalfLng FLOAT, \
                ThreeQuarterLat FLOAT, \
                ThreeQuarterLng FLOAT) \
                 ")
    cur.execute("CREATE TABLE Points \
                (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                MapMyRunId INT, \
                Lat FLOAT, \
                Lng FLOAT) \
                 ")