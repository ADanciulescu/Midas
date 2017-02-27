from snap_fetcher import SnapFetcher
from db_manager import DBManager
import table_names
import threading
import time

def run_sf(tn):
	sf = SnapFetcher(tn)
	sf.run()

for tn in table_names.snap_tables:
	d = threading.Thread(target = run_sf, args = (tn,))
	d.start()


