import json
import sqlite3

class DBManager:

	INSTANCE = None

	INTEGER = "INTEGER"
	REAL = "REAL"
	TEXT = "TEXT"
	NOT_NULL = "NOT NULL"
	
	def __init__(self):
		self.sqlfile = "./db/currencies.sqlite"
		self.conn = sqlite3.connect(self.sqlfile)

	@classmethod
	def get_instance(cls):
		if cls.INSTANCE is None:
			cls.INSTANCE = cls()
			cls.INSTANCE.open()
		return cls.INSTANCE


	def open(self):
		self.conn = sqlite3.connect(self.sqlfile)

	##commit changes to db and close DBManager instance
	def save_and_close(self):
		self.conn.commit()

	def get_cursor(self):
		return self.conn.cursor()

	## drops the table by name
	@staticmethod	
	def drop_table(table_name):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		cursor.execute('DROP TABLE ' + table_name)
		db_manager.save_and_close()
	
	## drops all tables that contain the given string
	@staticmethod	
	def drop_matching_tables(s):
		db_manager = DBManager.get_instance()

		##fetch all tables
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		all_table_names = cursor.fetchall()

		for tn in all_table_names:
			if s in tn[0]:
				cursor.execute('DROP TABLE ' + tn[0])
		db_manager.save_and_close()

	##returns true if table exists otherwise false
	@staticmethod	
	def exists_table(table_name):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}'".format(tn = table_name)
		cursor.execute(exec_string)
		if cursor.fetchone() is not None:
			return True
		else:
			return False
		db_manager.save_and_close()
