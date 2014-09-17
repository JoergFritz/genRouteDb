import MySQLdb as mdb

# connect to database with running routes
con=mdb.connect(host="mysql.server",user="JoergFritz", \
            db="JoergFritz$runRoutes",passwd="you-wish")

cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT DISTINCT(CITY) FROM Tracks")
rows = cur.fetchall()

print rows

