import MySQLdb as mdb
import numpy as np
from helpers import geocode

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runTracks",passwd="you-wish")
cur = con.cursor(mdb.cursors.DictCursor)

# create Database for cities
cur.execute("DROP TABLE IF EXISTS Cities")
cur.execute("CREATE TABLE Cities \
            (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
            City VARCHAR(50), \
            Lat FLOAT(10,6),  \
            Lng FLOAT(10,6))  \
             ")

add_city = ("INSERT INTO Cities "
              "(City, Lat, Lng) "
              "VALUES (%(City)s, %(Lat)s, %(Lng)s)")

keyLocations=['Palo Alto, CA', 'Stanford, CA', 'East Palo Alto, CA', 'Mountain View, CA', 'Sunnyvale, CA', 'Menlo Park, CA']
lat = np.zeros(len(keyLocations))
lng = np.zeros(len(keyLocations))

for city in keyLocations:
    lat,lng,full_add,data = geocode(city)
    data_city = {
            'City': city,
            'Lat': lat,
            'Lng': lng,
    }
    cur.execute(add_city, data_city)

con.commit()

cur.close()
con.close()


