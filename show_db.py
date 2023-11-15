import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
from statistics import stdev
import make_db

client_id = '52daefbfe55b4f14baf2ca49a6ee745a'
client_secret = '5329ddcdb1624154bf94c8c230390867'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

dbname = ('test.db')
conn = sqlite3.connect(make_db.dbname)
cursor = conn.cursor()
df = pd.read_sql('SELECT * FROM params', conn)
print(df)

sql = """SELECT MAX(tempo) FROM params"""
for t in conn.execute(sql):
    print('max: ',t[0])
conn.commit()

list = []
sql = """SELECT acousticness FROM params"""
for t in cursor.execute(sql):
    list.append(t[0])
    #print(t[0])

average = sum(list)/len(list)
print('average: ', average)
std = stdev(list)
print('std:', std)
max_normal = average + (std*2)
print(max_normal)
min_normal = average - (std*2)
print(min_normal)

plt.hist(list)
plt.show()

sql = """SELECT name FROM params WHERE artist='Saucy Dog'"""
for t in cursor.execute(sql):
    print(t[0])

conn.close()