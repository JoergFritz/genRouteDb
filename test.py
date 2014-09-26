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
            db="JoergFritz$runRoutesTest",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)


# generate list with existing mapMyRunIds to avoid duplication
cur.execute("SELECT Id, MapMyRunId from Tracks LIMIT 100")
rowsTracks = cur.fetchall()
existIds = np.zeros(len(rowsTracks), dtype=np.int)
#existIds = np.zeros(len(rowsTracks))
for i in range(len(rowsTracks)):
    existIds[i] = rowsTracks[1]['MapMyRunId']
    print existIds[i]
