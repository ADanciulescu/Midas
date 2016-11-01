from datetime import date, datetime
import time

def date_to_timestamp(adr):
	year = int(adr.split("-")[0])
	month = int(adr.split("-")[1])
	day = int(adr.split("-")[2])
	dt = date(year, month, day)
	
	ts = int(time.mktime(dt.timetuple()))
	return ts 

def timestamp_to_date(ts):
	date = datetime.fromtimestamp(ts)
	return date.strftime('%Y-%m-%d')


