#cos類似度で比較
#10times_cos.pyで10回実行
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

idl = []  #指定したプレイリストの曲のID
count = -1
pl_data = sp.user_playlist('31ljsv2irs6y7cgnfg737awxg2fe','37i9dQZF1DWXX3HHYIWJwh')     ##引数１：自分のユーザーID　引数２：プレイリストID
for track in pl_data['tracks']['items']:
        try:
            id = track['track']['id']
            count = count + 1
        except TypeError:
            continue
        idl.append(id)

#入力に使う6曲を決めるために、乱数を生成し、music_id_listに入れる
music_id_list = []
for i in range(6):
    n = random.randint(0,count)
    #print(n)
    music_id_list.append(idl[n])

#default_playlist.txtの読み込み
pdl = {}
with open('default_playlist.txt') as d:
    for line in d:
        (k,v) = line.split()
        pdl[k] = v

#ファイルの生成と日付の書き込み
file = open("output_text_folder/" + sys.argv[1], 'w')
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
file.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+'\n')
file.write('score_cos.py'+'\n')
file.write(pl_data['name']+'  '+'https://open.spotify.com/playlist/'+pl_data['id']+'\n')

playlist_list = [pdl['p1'],pdl['p2'],pdl['p3'],pdl['p4'],pdl['p5'],pdl['p6'],pdl['p7'],pdl['p8'],pdl['p9'],pdl['p10'],
                pdl['p11'],pdl['p12'],pdl['p13'],pdl['p14'],pdl['p15'],pdl['p16'],pdl['p17'],pdl['p18'],pdl['p19'],pdl['p20'],
                pdl['p21'],pdl['p22'],pdl['p23'],pdl['p24'],pdl['p25'],pdl['p26'],pdl['p27'],pdl['p28'],pdl['p29'],pdl['p30'],
                pdl['p31'],pdl['p32'],pdl['p33'],pdl['p34'],pdl['p35'],pdl['p36'],pdl['p37'],pdl['p38'],pdl['p39'],pdl['p40'],
                pdl['p41'],pdl['p42'],pdl['p43'],pdl['p44'],pdl['p45'],pdl['p46'],pdl['p47']]
playlist_id_list = []
m_list = []

for i in music_id_list:
    result = sp.audio_features(i) #パラメータのデータ
    x = sp.track(i) #曲名やアーティスト名など
    #file.write(x['name']+' ('+x['artists'][0]['name']+')'+'\n')      #曲名の表示
    m = result[0]
    #print(m)
    m_list.append(m)
    m_str = json.dumps(m)           #ファイルに書き込むためにdictからstringに変換
    #file.write(m_str)               #曲のパラメーターの表示
    #file.write('\n')

D = 'danceability'
E = 'energy'
Lo = 'loudness'
S = 'speechiness'
A = 'acousticness'
Li = 'liveness'
V = 'valence'
T = 'tempo'
element_list = [D,E,S,A,Li,V,T]

#正規化   Mean Normalization
def d_normal(a):
    i = (a-0.59)/(0.9-0.1)
    return i

def e_normal(a):
    i = (a-0.76)/(1.0-0.4)
    return i

def s_normal(a):
    i = (a-0.07)/(0.28-0.02)
    return i

def a_normal(a):
    i = (a-0.13)/(0.9-0.01)
    return i

def Li_normal(a):
    i = (a-0.2)/(0.5-0.01)
    return i

def v_normal(a):
    i = (a-0.6)/(1-0.1)
    return i

def t_normal(a):                 
    i = (a-130.0)/(180.0-75.0)
    return i

avg_dict = {}

#入力曲の正規化前のパラメータの平均
def real_params(msc1,msc2,msc3,msc4,msc5,msc6):
    for element in element_list:
        if(element == D):
            dd = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
        elif(element == E):
            ee = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
        elif(element == S):
            ss = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
        elif(element == A):
            aa = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
        elif(element == Li):
            ll = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
        elif(element == V):
            vv = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
        elif (element == T):
            tt = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
    real = [dd,ee,ss,aa,ll,vv,tt]
    return real
import_real_params = real_params(m_list[0],m_list[1],m_list[2],m_list[3],m_list[4],m_list[5])   #入力曲の正規化前のパラメータの平均
#print('import_real_params: ',import_real_params)



#入力曲のパラメータの正規化とそれらの平均を求める
def make_seikika_element(msc1,msc2,msc3,msc4,msc5,msc6):   
    for element in element_list:
        if(element == D):
            msc1[element] = d_normal(msc1[element])
            msc2[element] = d_normal(msc2[element])
            msc3[element] = d_normal(msc3[element])
            msc4[element] = d_normal(msc4[element])
            msc5[element] = d_normal(msc5[element])
            msc6[element] = d_normal(msc6[element])
        elif(element == E):
            msc1[element] = e_normal(msc1[element])
            msc2[element] = e_normal(msc2[element])
            msc3[element] = e_normal(msc3[element])
            msc4[element] = e_normal(msc4[element])
            msc5[element] = e_normal(msc5[element])
            msc6[element] = e_normal(msc6[element])
        elif(element == S):
            msc1[element] = s_normal(msc1[element])
            msc2[element] = s_normal(msc2[element])
            msc3[element] = s_normal(msc3[element])
            msc4[element] = s_normal(msc4[element])
            msc5[element] = s_normal(msc5[element])
            msc6[element] = s_normal(msc6[element])
        elif(element == A):
            aa = (msc1[element]+msc2[element]+msc3[element]+msc4[element]+msc5[element]+msc6[element]) / 6 #正規化前のパラメータの平均
            msc1[element] = a_normal(msc1[element])
            msc2[element] = a_normal(msc2[element])
            msc3[element] = a_normal(msc3[element])
            msc4[element] = a_normal(msc4[element])
            msc5[element] = a_normal(msc5[element])
            msc6[element] = a_normal(msc6[element])
        elif(element == Li):
            msc1[element] = Li_normal(msc1[element])
            msc2[element] = Li_normal(msc2[element])
            msc3[element] = Li_normal(msc3[element])
            msc4[element] = Li_normal(msc4[element])
            msc5[element] = Li_normal(msc5[element])
            msc6[element] = Li_normal(msc6[element])
        elif(element == V):
            msc1[element] = v_normal(msc1[element])
            msc2[element] = v_normal(msc2[element])
            msc3[element] = v_normal(msc3[element])
            msc4[element] = v_normal(msc4[element])
            msc5[element] = v_normal(msc5[element])
            msc6[element] = v_normal(msc6[element])
        elif (element == T):
            msc1[element] = t_normal(msc1[element])
            msc2[element] = t_normal(msc2[element])
            msc3[element] = t_normal(msc3[element])
            msc4[element] = t_normal(msc4[element])
            msc5[element] = t_normal(msc5[element])
            msc6[element] = t_normal(msc6[element])
        element_data = [msc1[element], msc2[element],msc3[element],msc4[element],msc5[element],msc6[element]]
        avg = np.mean(element_data)
        avg = round(avg,3)
        avg_dict[element] = avg #正規化後の平均のリスト
make_seikika_element(m_list[0],m_list[1],m_list[2],m_list[3],m_list[4],m_list[5])
#print("avg_dict:", avg_dict)

#それぞれのパラメータの正規化後の平均（グラフ化）
D_avg = avg_dict[D]
E_avg = avg_dict[E]
S_avg = avg_dict[S]
A_avg = avg_dict[A]
Li_avg = avg_dict[Li]
V_avg = avg_dict[V]
T_avg = avg_dict[T]
import_music_average= [D_avg,E_avg,S_avg,A_avg,Li_avg,V_avg,T_avg]
#print("import_music_average: ",import_music_average)

str_dict = json.dumps(avg_dict)
file.write('正規化後のパラメータの平均'+str_dict+'\n')        #入力した６曲の平均の辞書リスト

#平均パラメータとプレイリスト内の曲のコサイン類似度の計算 
def sim_distance(avg,music):
    music = np.array(music)
    distance = np.dot(avg, music) / (np.linalg.norm(avg) * np.linalg.norm(music))
    return distance
#print(sim_distance(import_music_average,a))

features = []
id_list = []
feature_list = []
id_yuk = {}                  #曲のIDとユークリッド距離の値を持ったdict
match_list = []              #類似度が高い10曲のリスト

#正規化前の値を入れる配列
real_d = []
real_e = []
real_s = []
real_a = []
real_li = []
real_v = []
real_t = []

musiccount = 0
file.write('--------------<recommend songs>-----------------\n')
for a in range(47):
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
        musiccount = musiccount + 1
        for e in element_list:
            if(e == D):
                real_d.append(feature[e])
                feature[e] = d_normal(feature[e])
                feature_list.append(feature[e])
            elif(e == E):
                real_e.append(feature[e])
                feature[e] = e_normal(feature[e])
                feature_list.append(feature[e])
            elif(e == S):
                real_s.append(feature[e])
                feature[e] = s_normal(feature[e])
                feature_list.append(feature[e])
            elif(e == A):
                real_a.append(feature[e])
                feature[e] = a_normal(feature[e])
                feature_list.append(feature[e])
            elif(e == Li):
                real_li.append(feature[e])
                feature[e] = Li_normal(feature[e])
                feature_list.append(feature[e])
            elif(e == V):
                real_v.append(feature[e])
                feature[e] = v_normal(feature[e])
                feature_list.append(feature[e])
            elif(e == T):
                real_t.append(feature[e])
                feature[e] = t_normal(feature[e])
                feature_list.append(feature[e])
        id_yuk[feature['id']] = sim_distance(import_music_average,feature_list)
        feature_list.clear()
file.write('\n')
#print(musiccount)

real_d_avarege = np.mean(real_d)
real_e_avarege = np.mean(real_d)
real_s_avarege = np.mean(real_d)
real_a_avarege = np.mean(real_d)
real_li_avarege = np.mean(real_d)
real_v_avarege = np.mean(real_d)
real_t_avarege = np.mean(real_d)

recommned_real_params = [real_d_avarege,real_e_avarege,real_s_avarege,real_a_avarege,real_li_avarege,real_v_avarege,real_t_avarege]
#print('recommned_real_params: ', recommned_real_params)

#cos類似度が大きい(1に近い)順に並んだリスト
sorted_id_yuk = sorted(id_yuk.items(), key = lambda x:x[1], reverse=True)

for i in range(20):
    match_list.append(sorted_id_yuk[i][0])


match_artists_list = []
for m in match_list:
    a = sp.track(m)
    file.write('name: '+a['name']+'('+a['artists'][0]['name']+')'+'    https://open.spotify.com/track/'+a['id']+'\n')  #最終的にマッチした曲名を表示
    match_artists_list.append(a['artists'][0]['id'])

#スコア（レコメンド１０曲が入力を選んだプレイリスト内にいくつ含まれているかをスコアとする）
#idl -> プレイリストのすべての曲のID   match_list -> レコメンド１０曲のID
file.write('------------------<score>-----------------------'+'\n')
score = 0
for i in idl:
    result = i in match_list
    if(result == True):
        score = score + 1
        a = sp.track(i)
        file.write(a['name'])
        file.write('  '+'https://open.spotify.com/track/'+i+'\n')

score = str(score)
file.write('score: '+score)
print('score: ',score)
