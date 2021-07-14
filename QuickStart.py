#from pydrive.auth import GoogleAuth
import file_actions
import google_actions
import os
import time
from dateutil.parser import parse
from pytz import timezone
import main
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()

filetime = parse(time.ctime(os.path.getmtime('holi.txt')))
utcfiletime = filetime.replace(tzinfo = timezone('UTC'))

drive_files = main.manage_drive_actions()
drive_time = parse(drive_files[4]['modified_date'])
print(drive_time)
print(utcfiletime)
print(drive_time.timestamp())
print(utcfiletime.timestamp())


print(utcfiletime.timestamp() + 14400 > drive_time.timestamp())
