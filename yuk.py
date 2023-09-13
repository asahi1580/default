#ユークリッド距離、パラメータ７つ

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

import make_db

client_id = '52daefbfe55b4f14baf2ca49a6ee745a'
client_secret = '5329ddcdb1624154bf94c8c230390867'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#ファイルの生成と日付の書き込み
file = open("output_text_folder/" + sys.argv[1], 'w')
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
file.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+'\n')
file.write('yuk.py'+'\n')

#auto_import_music.txtの読み込み
idl = {}
with open('auto_import_music.txt') as i:
    for line in i:
        (k,v) = line.split()
        idl[k] = v
music_list = [idl['m1'],idl['m2'],idl['m3'],idl['m4'],idl['m5'],idl['m6']]
music_id_list = []
m_list = []
for i in music_list:
    pl = i[31:]
    if ('?' in pl):
        pl_idx = pl.find('?')
        pl = pl[:pl_idx]
    music_id_list.append(pl)
    result = sp.audio_features(pl) #パラメータのデータ
    x = sp.track(pl) #曲名やアーティスト名など
    file.write(x['name']+' ('+x['artists'][0]['name']+')'+'\n')      #曲名の表示
    m = result[0]
    #print(m)
    m_list.append(m)
    m_str = json.dumps(m)           #ファイルに書き込むためにdictからstringに変換
    file.write(m_str)               #曲のパラメーターの表示
    file.write('\n')

D = 'danceability'
E = 'energy'
Lo = 'loudness'
S = 'speechiness'
A = 'acousticness'
Li = 'liveness'
V = 'valence'
T = 'tempo'
element_list = [D,E,S,A,Li,V,T]

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
print('import_real_params: ',import_real_params)

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
print("avg_dict:", avg_dict)
#それぞれのパラメータの正規化後の平均
D_avg = avg_dict[D]
E_avg = avg_dict[E]
S_avg = avg_dict[S]
A_avg = avg_dict[A]
Li_avg = avg_dict[Li]
V_avg = avg_dict[V]
T_avg = avg_dict[T]
import_music_average= [D_avg,E_avg,S_avg,A_avg,Li_avg,V_avg,T_avg]
print("import_music_average: ",import_music_average)

dbname = ('test.db')
conn = sqlite3.connect(make_db.dbname)
cursor = conn.cursor()

def sim_distance(avg,music):
    music = np.array(music)
    distance = np.linalg.norm(avg-music)
    return distance


sql = """SELECT id FROM params """
id_array = []
d_array = []
e_array = []
s_array = []
a_array = []
Li_array = []
v_array = []
t_array = []

count = 0
for t in cursor.execute(sql):
    id_array.append(t[0])
    count = count + 1

sql = """SELECT danceability FROM params"""
for t in cursor.execute(sql):
    t = d_normal(t[0])
    d_array.append(t)

sql = """SELECT energy FROM params"""
for t in cursor.execute(sql):
    t = e_normal(t[0])
    e_array.append(t)

sql = """SELECT speechiness FROM params"""
for t in cursor.execute(sql):
    t = s_normal(t[0])
    s_array.append(t)

sql = """SELECT acousticness FROM params"""
for t in cursor.execute(sql):
    t = a_normal(t[0])
    a_array.append(t)

sql = """SELECT liveness FROM params"""
for t in cursor.execute(sql):
    t = Li_normal(t[0])
    Li_array.append(t)

sql = """SELECT valence FROM params"""
for t in cursor.execute(sql):
    t = v_normal(t[0])
    v_array.append(t)

sql = """SELECT tempo FROM params"""
for t in cursor.execute(sql):
    t = t_normal(t[0])
    t_array.append(t)

id_yuk = {}
feature_list = []
for i in range(count):
    feature_id_list = [id_array[i],d_array[i],e_array[i],s_array[i],a_array[i],Li_array[i],v_array[i],t_array[i]]
    feature_list = [d_array[i],e_array[i],s_array[i],a_array[i],Li_array[i],v_array[i],t_array[i]]
    #print(feature_list)
    id_yuk[feature_id_list[0]] = sim_distance(import_music_average, feature_list)  #曲のIDとユークリッド距離

match_list = []     #類似度が高い10曲のリスト
#ユークリッド距離が近い順に並んだリスト
sorted_id_yuk = sorted(id_yuk.items(), key = lambda x:x[1])
for i in range(10):
    match_list.append(sorted_id_yuk[i][0])

#レコメンドされた曲のパラメータ （グラフ）
recommend_D_list = []
recommend_E_list = []
recommend_S_list = []
recommend_A_list = []
recommend_Li_list = []
recommend_V_list = []
recommend_T_list = []

for m in match_list:
    a = sp.track(m)
    file.write('name: '+a['name']+'('+a['artists'][0]['name']+')'+'    https://open.spotify.com/track/'+a['id']+'\n')  #最終的にマッチした曲名を表示
    result = sp.audio_features(m)
    recommend_D_list.append(d_normal(result[0][D]))
    recommend_E_list.append(e_normal(result[0][E]))
    recommend_S_list.append(s_normal(result[0][S]))
    recommend_A_list.append(a_normal(result[0][A]))
    recommend_Li_list.append(Li_normal(result[0][Li]))
    recommend_V_list.append(v_normal(result[0][V]))
    recommend_T_list.append(t_normal(result[0][T]))

recommend_average_D = np.mean(recommend_D_list)
recommend_average_E = np.mean(recommend_E_list)
recommend_average_S = np.mean(recommend_S_list)
recommend_average_A = np.mean(recommend_A_list)
recommend_average_Li = np.mean(recommend_Li_list)
recommend_average_V = np.mean(recommend_V_list)
recommend_average_T = np.mean(recommend_T_list)

recommend_music_average = [recommend_average_D,recommend_average_E,recommend_average_S,recommend_average_A,recommend_average_Li,recommend_average_V,recommend_average_T]

print(recommend_D_list)
#グラフ生成
x_1 = [0, 1, 2, 3, 4, 5, 6]            # 系列 1 をプロットするx座標
x_2 = [0.2, 1.2, 2.2, 3.2, 4.2, 5.2, 6.2]  # 系列 2 をプロットするx座標
plt.bar(x_1, import_music_average, label='import', width=0.2)
plt.bar(x_2, recommend_music_average, label='recommend',width = -0.2)
plt.xticks(x_1, element_list)
plt.grid(True)
plt.legend()
plt.show()

music_id = '6WYirtXQjDJpCQkv4XTBxY'
result = sp.audio_features(music_id)
#print(result[0][D])
conn.close()