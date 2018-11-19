import psycopg2
import pprint

conn_string = "host='green-z.cs.rpi.edu' dbname='index' user='ranking' password='ranking'"

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


cursor.execute("SELECT * FROM index;")

records = cursor.fetchall()

pprint.pprint(records)

print(type(records[0]))
