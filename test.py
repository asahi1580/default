import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np
import math
import sys
import datetime
import pytz
import collections
import matplotlib.pylab as plt
import random

client_id = '52daefbfe55b4f14baf2ca49a6ee745a'
client_secret = '5329ddcdb1624154bf94c8c230390867'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


'''
pdl = {}
with open('default_playlist.txt') as d:
    for line in d:
        (k,v) = line.split()
        pdl[k] = v

playlist_list = [pdl['p1'],pdl['p2'],pdl['p3'],pdl['p4'],pdl['p5'],pdl['p6'],pdl['p7'],pdl['p8'],pdl['p9'],pdl['p10'],
                pdl['p11'],pdl['p12'],pdl['p13'],pdl['p14'],pdl['p15'],pdl['p16'],pdl['p17'],pdl['p18'],pdl['p19'],pdl['p20'],
                pdl['p21'],pdl['p22'],pdl['p23'],pdl['p24'],pdl['p25'],pdl['p26'],pdl['p27'],pdl['p28'],pdl['p29'],pdl['p30'],
                pdl['p31'],pdl['p32'],pdl['p33'],pdl['p34'],pdl['p35'],pdl['p36'],pdl['p37'],pdl['p38'],pdl['p39'],pdl['p40'],
                pdl['p41'],pdl['p42'],pdl['p43'],pdl['p44'],pdl['p45'],pdl['p46'],pdl['p47']]

features = []
id_list = []
feature_list = []
id_yuk = {}                  #曲のIDとユークリッド距離の値を持ったdict
match_list = [] 

for a in range(1):
    playlist_data = sp.user_playlist('31ljsv2irs6y7cgnfg737awxg2fe',playlist_list[a])     ##引数１：自分のユーザーID　引数２：プレイリストID
    features.clear()
    id_list.clear()
    #file.write(playlist_data['name']+'  '+'https://open.spotify.com/playlist/'+playlist_list[a]+'\n')
    #プレイリストの曲のIDをfeaturesにいれる 
    for track in playlist_data['tracks']['items']:
        try:
            id = track['track']['id']
        except TypeError:
            continue
        id_list.append(id)
    features.extend(sp.audio_features(id_list))
    
    #正規化前のパラメータの取得
    #パラメータの正規化
    
    for feature in features:
        
        i = sp.track(feature['id'])
        print(i['album']['artists'][0]['name'])
        #artist_id = i['artists'][0]['name']
        #print(artist_id)
#result = sp.track('1TYSgBF0FdqmiddlHsdRSk')
#print(result['album']['artists'][0]['name'])
'''

print(sp.audio_features('1gACe11pZiy8Xv3SY0ocyz'))