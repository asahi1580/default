#曲のID検索プログラム
#第一引数にその曲のタイトルを入力して実行
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import datetime
import pytz

client_id = '52daefbfe55b4f14baf2ca49a6ee745a'
client_secret = '5329ddcdb1624154bf94c8c230390867'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

import_file = open("auto_import_music.txt", 'w')
info_file = open("output_text_folder/" + "info.txt", 'w')

dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
info_file.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+'\n')

search_str1 = sys.argv[1]
search_str2 = sys.argv[2]
search_str3 = sys.argv[3]
search_str4 = sys.argv[4]
search_str5 = sys.argv[5]
search_str6 = sys.argv[6]

results1 = sp.search(q=search_str1, type='track', limit=10, market='JP')
import_file.write('m1 '+'https://open.spotify.com/track/'+results1['tracks']['items'][0]['id']+'\n')

info_file.write('「'+search_str1+'」'+'の検索結果'+'\n')
for idx, track in enumerate(results1['tracks']['items']):
    info_file.write(track['name']+'('+track['artists'][0]['name']+')'+'    url:'+'https://open.spotify.com/track/'+track['id']+'\n')
info_file.write('\n')
info_file.write('\n')


results2 = sp.search(q=search_str2, type='track', limit=10, market='JP')
import_file.write('m2 '+'https://open.spotify.com/track/'+results2['tracks']['items'][0]['id']+'\n')

results2 = sp.search(q=search_str2, type='track', limit=10, market='JP')
info_file.write('「'+search_str2+'」'+'の検索結果'+'\n')
for idx, track in enumerate(results2['tracks']['items']):
    info_file.write(track['name']+'('+track['artists'][0]['name']+')'+'    url:'+'https://open.spotify.com/track/'+track['id']+'\n')
info_file.write('\n')
info_file.write('\n')


results3 = sp.search(q=search_str3, type='track', limit=10, market='JP')
import_file.write('m3 '+'https://open.spotify.com/track/'+results3['tracks']['items'][0]['id']+'\n')

results3 = sp.search(q=search_str3, type='track', limit=10, market='JP')
info_file.write('「'+search_str3+'」'+'の検索結果'+'\n')
for idx, track in enumerate(results3['tracks']['items']):
    info_file.write(track['name']+'('+track['artists'][0]['name']+')'+'    url:'+'https://open.spotify.com/track/'+track['id']+'\n')
info_file.write('\n')
info_file.write('\n')


results4 = sp.search(q=search_str4, type='track', limit=10, market='JP')
import_file.write('m4 '+'https://open.spotify.com/track/'+results4['tracks']['items'][0]['id']+'\n')

results4 = sp.search(q=search_str4, type='track', limit=10, market='JP')
info_file.write('「'+search_str4+'」'+'の検索結果'+'\n')
for idx, track in enumerate(results4['tracks']['items']):
    info_file.write(track['name']+'('+track['artists'][0]['name']+')'+'    url:'+'https://open.spotify.com/track/'+track['id']+'\n')
info_file.write('\n')
info_file.write('\n')


results5 = sp.search(q=search_str5, type='track', limit=10, market='JP')
import_file.write('m5 '+'https://open.spotify.com/track/'+results5['tracks']['items'][0]['id']+'\n')

results5 = sp.search(q=search_str5, type='track', limit=10, market='JP')
info_file.write('「'+search_str5+'」'+'の検索結果'+'\n')
for idx, track in enumerate(results5['tracks']['items']):
    info_file.write(track['name']+'('+track['artists'][0]['name']+')'+'    url:'+'https://open.spotify.com/track/'+track['id']+'\n')
info_file.write('\n')
info_file.write('\n')


results6 = sp.search(q=search_str6, type='track', limit=10, market='JP')
import_file.write('m6 '+'https://open.spotify.com/track/'+results6['tracks']['items'][0]['id']+'\n')

results6 = sp.search(q=search_str6, type='track', limit=10, market='JP')
info_file.write('「'+search_str6+'」'+'の検索結果'+'\n')
for idx, track in enumerate(results6['tracks']['items']):
    info_file.write(track['name']+'('+track['artists'][0]['name']+')'+'    url:'+'https://open.spotify.com/track/'+track['id']+'\n')
info_file.write('\n')
info_file.write('\n')