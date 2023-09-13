#データベースに曲を追加
#プレイリスト単位で行う  add_playlistを書き換え
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

#add_playlist.txtの読み込み
pdl = {}
with open ('add_playlist.txt') as d:
    for line in d:
        (k,v) = line.split()
        pdl[k] = v
playlist_list = [pdl['p1'],pdl['p2'],pdl['p3'],pdl['p4'],pdl['p5'],pdl['p6'],pdl['p7'],pdl['p8'],pdl['p9'],pdl['p10']]

dbname = ('test.db')
conn = sqlite3.connect(make_db.dbname)
cursor = conn.cursor()
db_idlist = []
sql = """SELECT id FROM params"""
for t in cursor.execute(sql):
    db_idlist.append(t[0])

print(len(db_idlist))
add_idlist = []  #データベースに追加する曲のIDリスト
for i in range(10):
    pl_data = sp.user_playlist('31ljsv2irs6y7cgnfg737awxg2fe',playlist_list[i])     ##引数１：自分のユーザーID 引数２：プレイリストID
    for track in pl_data['tracks']['items']:
        try:
            id = track['track']['id']
            #print(id)
        except TypeError:
            continue
        result = id in db_idlist
        if(result == False):
            add_idlist.append(id)

D = 'danceability'
E = 'energy'
Lo = 'loudness'
S = 'speechiness'
A = 'acousticness'
Li = 'liveness'
V = 'valence'
T = 'tempo'
#add_idlistの曲をデータベースに追加
sql = """INSERT INTO params VALUES(?,?,?,?,?,?,?,?,?,?)"""
for id in add_idlist:
    x = sp.track(id)
    name = x['name']
    artist = x['artists'][0]['name']
    feature = sp.audio_features(id)
    result = feature[0]
    try:
        data = (id, name, artist, result[D], result[E],  result[S], result[A], result[Li], result[V], result[T])
    except TypeError:
        continue
    cursor.execute(sql, data)
    conn.commit()