import json
import sqlite3

class DBManager:

	INTEGER = "INTEGER"
	REAL = "REAL"
	NOT_NULL = "NOT NULL"
	
	def __init__(self):
		self.sqlfile = "./db/currencies.sqlite"
		self.conn = sqlite3.connect(self.sqlfile)
		
	##commit changes to db and close DBManager instance
	def save_and_close(self):
		self.conn.commit()
		self.conn.close()

	def get_cursor(self):
		return self.conn.cursor()

	## drops the table by name
	@staticmethod	
	def drop_table(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		cursor.execute('DROP TABLE ' + table_name)
		db_manager.save_and_close()

	##returns true if table exists otherwise false
	@staticmethod	
	def exists_table(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}'".format(tn = table_name)
		cursor.execute(exec_string)
		if cursor.fetchone() is not None:
			return True
		else:
			return False
		db_manager.save_and_close()
