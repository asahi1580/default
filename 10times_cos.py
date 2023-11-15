import os
import datetime
import pytz

dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

for i in range(10):
    os.system('python cos_score.py '+dt_now.strftime('%Y%m%d%H%M%S')+'_'+str(i)+'_cos'+'.txt')