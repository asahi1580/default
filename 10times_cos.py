import os
import datetime
import pytz

dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

for i in range(10):
    os.system('python score_cos.py '+dt_now.strftime('%Y%m%d')+'_'+str(i)+'_cos'+'.txt')