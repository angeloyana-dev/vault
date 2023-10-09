import base64
from cryptography.fernet import Fernet

def get_key(master_key):
	key = master_key + '==================================='
	return base64.urlsafe_b64encode(key[:32].encode('utf8'))
	
class Cipher:
	def __init__(self, master_key):
		self.cipher = Fernet(get_key(master_key))
		
	def encrypt(self, data):
		encrypted_data = self.cipher.encrypt(data.encode('utf8'))
		return encrypted_data.hex()
	
	def decrypt(self, data):
		decrypted_data = self.cipher.decrypt(bytes.fromhex(data))
		return decrypted_data.decode('utf8')