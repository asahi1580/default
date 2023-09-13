import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_id = '52daefbfe55b4f14baf2ca49a6ee745a'
client_secret = '5329ddcdb1624154bf94c8c230390867'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

dbname = ('test.db')

if __name__=="__main__":
    conn = sqlite3.connect(dbname, isolation_level=None)
    cursor = conn.cursor()

    sql = """DROP TABLE if exists params"""
    conn.execute(sql)
    conn.commit()

    sql = """CREATE TABLE IF NOT EXISTS params(id, name, artist, danceability, energy, speechiness, acousticness, liveness, valence, tempo)"""
    cursor.execute(sql)
    conn.commit()

    sql = """INSERT INTO params VALUES(?,?,?,?,?,?,?,?,?,?)"""

    idl = []  #指定したプレイリストの曲のID
    count = -1

    #default_playlist.txtの読み込み
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

    for i in range(47):
        pl_data = sp.user_playlist('31ljsv2irs6y7cgnfg737awxg2fe',playlist_list[i])     ##引数１：自分のユーザーID 引数２：プレイリストID
        for track in pl_data['tracks']['items']:
            try:
                id = track['track']['id']
                print(id)
                count = count + 1
            except TypeError:
                continue
            result = id in idl
            if(result == False):
                idl.append(id)

    print('count: ',count)

    D = 'danceability'
    E = 'energy'
    Lo = 'loudness'
    S = 'speechiness'
    A = 'acousticness'
    Li = 'liveness'
    V = 'valence'
    T = 'tempo'

    for id in idl:
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


    conn = sqlite3.connect(dbname)
    df = pd.read_sql('SELECT * FROM params', conn)
    print(df)

    conn.close()