import sqlite3, json
from vault import credentials_db_path
from vault.modules.cipher import Cipher

class DataManager:
    def __init__(self, key):
        self.conn = sqlite3.connect(credentials_db_path)
        self.c = self.conn.cursor()
        self.cipher = Cipher(key)
        self.c.execute("""CREATE TABLE IF NOT EXISTS credentials (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              platform_name TEXT,
                              credential TEXT
                          )""")
        
    def _format_credentials_list(self, credential):
        pairs = json.loads(credential[2])
        for key, value in list(pairs.items()):
            decrypted_value = self.cipher.decrypt(value)
            pairs[key] = decrypted_value
            
        return {
            'platform_name': credential[1],
            'pairs': pairs
        }
        
    def add(self, credential):
        platform_name = credential["platform_name"]
        pairs = credential["pairs"]
        for key, value in list(pairs.items()):
            encrypted_value = self.cipher.encrypt(value)
            pairs[key] = encrypted_value
        
        self.c.execute("INSERT INTO credentials (platform_name, credential) VALUES (?,?)", (platform_name, json.dumps(pairs)))
        self.conn.commit()
        
    def get_all(self):
        self.c.execute("SELECT * FROM credentials")
        credentials = self.c.fetchall()
        if not credentials: return None
        return list(map(self._format_credentials_list, credentials))
        
    def get_all_names(self):
        self.c.execute("SELECT platform_name FROM credentials")
        names = self.c.fetchall()
        if not names: return None
        return [name[0] for name in names]
        
    def get_one(self, platform_name):
        self.c.execute("SELECT * FROM credentials WHERE platform_name = ?", (platform_name,))
        credential = self.c.fetchone()
        return self._format_credentials_list(credential)
        
    def update_one(self, platform_name, pairs):
        for key, value in list(pairs.items()):
            encrypted_value = self.cipher.encrypt(value)
            pairs[key] = encrypted_value
            
        self.c.execute("UPDATE credentials SET credential = ? WHERE platform_name = ?",
                        (json.dumps(pairs), platform_name))
        self.conn.commit()
        
    def delete_one(self, platform_name):
        self.c.execute("DELETE FROM credentials WHERE platform_name = ?", (platform_name,))
        self.conn.commit()