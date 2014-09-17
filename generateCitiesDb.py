import MySQLdb as mdb
import pandas as pd
import numpy as np
from helpers import geocode

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")

cur = con.cursor(mdb.cursors.DictCursor)

keyLocations=['Palo Alto, CA', 'Stanford, CA', 'East Palo Alto, CA', 'Mountain View, CA', 'Sunnyvale, CA', 'Menlo Park, CA']
lat = np.zeros(len(keyLocations))
lng = np.zeros(len(keyLocations))

for i in range(len(keyLocations)):
    lat[i],lng[i],full_add,data = geocode(keyLocations[i])

data = { 'city': keyLocations,
          'lat': lat,
          'lng': lng}

citiesData = pd.DataFrame(data, columns=['city', 'lat', 'lng'])

print citiesData




