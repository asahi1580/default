import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

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

sql = """SELECT name FROM params WHERE artist='Mrs. GREEN APPLE'"""
for t in cursor.execute(sql):
    print(t)

conn.close()