import MySQLdb as mdb
import numpy as np
from helpers import geocode

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutesTest",passwd="you-wish")
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


keyLocations=['Stanford','Mountain View','Belmont','Milpitas','Menlo Park','San Bruno',
    'East Palo Alto','Cupertino','Redwood City','San Carlos','Millbrae','San Jose Japantown',
    'South San Mateo','Palo Alto','Los Altos','North San Jose','San Mateo','North Los Altos',
    'Santa Clara','North Santa Clara','East Palo Alto','Hillsborough','South San Francisco',
    'Sunnyvale']
#lat = np.zeros(len(keyLocations))
#lng = np.zeros(len(keyLocations))
lat = [37.4249378,37.4038194,37.523231,37.432876,37.4510044,37.6263344,
    37.463793,37.331411,37.486322,37.498567,37.5983528,37.3541108,
    37.535106,37.4291488,37.3650347,37.3881531,37.5663668,37.3903822,
    37.3542997,37.404375,37.390773,37.566822,37.6671504,
    37.3770751]
lng = [-122.1703835,-122.081267,-122.276572,-121.907099,-122.1916764,-122.4261976,
    -122.151508,-122.030315,-122.229594,-122.291272,-122.3874685,-121.8896426,
    -122.335093,-122.1225688,-122.0870202,-121.9244973,-122.3192046,-122.1263072,
    -121.984147,-121.975405,-121.848433,-122.362346,-122.4275131,
    -122.0354522]


n = 0
for city in keyLocations:
    #lat,lng,full_add,data = geocode(city)
    data_city = {
            'City': city,
            'Lat': lat[n],
            'Lng': lng[n],
    }
    cur.execute(add_city, data_city)
    n = n+1

con.commit()

cur.close()
con.close()


