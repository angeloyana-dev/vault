import sqlite3
from modules.cipher import Cipher

class DataManager:
	def __init__(self, master_key, credentials_path):
		self.cipher = Cipher(master_key)
		self.conn = sqlite3.connect(credentials_path)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS keys
		                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, key TEXT)""")
		self.c.execute("""CREATE TABLE IF NOT EXISTS multiples
		                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, password TEXT)""")
		self.conn.commit()
		
	# Decrypts and reformat to obj
	def _formatkey(self, row):
		decrypted_key = self.cipher.decrypt(row[2])
		return { 'name': row[1], 'key': decrypted_key }
	
	def _formatmultiple(self, row):
		decrypted_username = self.cipher.decrypt(row[2])
		decrypted_password = self.cipher.decrypt(row[3])
		
		return {
			'name': row[1],
			'username': decrypted_username,
			'password': decrypted_password
		}
		
	def insert(self, name, key=False, multiple=False):
		if key:
			encrypted_key = self.cipher.encrypt(key)
			self.c.execute("""INSERT INTO keys (name, key) VALUES
			                  (?, ?)""", (name, encrypted_key))
		elif multiple:
			encrypted_username = self.cipher.encrypt(multiple['username'])
			encrypted_password = self.cipher.encrypt(multiple['password'])
			self.c.execute("""INSERT INTO multiples (name, username, password) VALUES
			                  (?, ?, ?)""", (name, encrypted_username, encrypted_password))
		self.conn.commit()
		
	def select(self, which):
		def get_keys():
			self.c.execute('SELECT * FROM keys')
			rows = self.c.fetchall()
			if not rows:
				return []
			rows = map(self._formatkey, rows)
			return list(rows)
		
		def get_multiples():
			self.c.execute('SELECT * FROM multiples')
			rows = self.c.fetchall()
			if not rows:
				return []
			rows = map(self._formatmultiple, rows)
			return list(rows)
			
		if which == 'keys':
			return get_keys()
		elif which == 'multiples':
			return get_multiples()