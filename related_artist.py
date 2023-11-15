#乱数で決まった5曲から似ているアーティストを検索し、
#データベースからそのアーティストの曲をレコメンド

import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import datetime
import sys
import pytz
import json
import matplotlib.pylab as plt
import random
import collections

import make_db

client_id = '52daefbfe55b4f14baf2ca49a6ee745a'
client_secret = '5329ddcdb1624154bf94c8c230390867'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#ファイルの生成と日付の書き込み
file = open("output_text_folder/" + sys.argv[1], 'w')
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
file.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+'\n')
file.write('yuk_score.py'+'\n')

idl = []  #指定したプレイリストの曲のID
count = -1
pl_data = sp.user_playlist('31ljsv2irs6y7cgnfg737awxg2fe','24NM1KCr8TWvD134lA5v1X')     ##引数１：自分のユーザーID　引数２：プレイリストID
for track in pl_data['tracks']['items']:
        try:
            id = track['track']['id']
            count = count + 1
        except TypeError:
            continue
        idl.append(id)

#入力に使う5曲を決めるために、乱数を生成し、music_id_listに入れる
music_id_list = []
for i in range(5):
    n = random.randint(0,count)
    #print(n)
    music_id_list.append(idl[n])

file.write(pl_data['name']+'  '+'https://open.spotify.com/playlist/'+pl_data['id']+'\n')
m_list = []
artist_id = []
#乱数によってえらばれた曲のパラメータをファイルに書き込み
for i in music_id_list:
    result = sp.audio_features(i) #パラメータのデータ
    x = sp.track(i) #曲名やアーティスト名など
    file.write(x['name']+' ('+x['artists'][0]['name']+')'+'\n')      #曲名の表示
    artist_id.append(x['artists'][0]['id'])
    m = result[0]
    #print(m)
    m_list.append(m)
    m_str = json.dumps(m)           #ファイルに書き込むためにdictからstringに変換
    file.write(m_str)               #曲のパラメーターの表示
    file.write('\n')

#print(artist_id)
recommend_artists = []        #似ているアーティストの名前
dupl = []   #recommend_artistsで重複しているアーティストの名前と頻度
dupl_name = []   #recommend_artistsで重複しているアーティストの名前
for a in artist_id:
    result = sp.artist_related_artists(a)
    for artist in result['artists']:
        #print(artist['name'])
        recommend_artists.append(artist['name'])
collection = collections.Counter(recommend_artists)
dupl.append(collection.most_common(10))
#print(dupl[0])

for i in range(10):
    dupl_name.append(dupl[0][i][0])
print(dupl_name)

dbname = ('test.db')
conn = sqlite3.connect(make_db.dbname)
cursor = conn.cursor()

match_list = []
#データベースからアーティスト名がdupl_nameと同じ曲を探す
for i in range(10):
    for t in cursor.execute("""SELECT id,name FROM params WHERE artist=?""",(dupl_name[i],)):
        match_list.append(t[0])
        #print(t[1])

match_list_10 = []
for i in range(10):
    match_list_10.append(match_list[i])
print(match_list_10)


file.write('------------------<score>-----------------------'+'\n')
score = 0
for i in idl:
    result = i in match_list_10
    if(result == True):
        score = score + 1
        a = sp.track(i)
        file.write(a['name'])
        file.write('  '+'https://open.spotify.com/track/'+i+'\n')
score = str(score)
file.write('score: '+score)
print('score: ',score)