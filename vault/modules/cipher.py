import base64
from cryptography.fernet import Fernet

def get_key(key):
    key = (key + '*' * 32)[:32]
    return base64.urlsafe_b64encode(key.encode())

class Cipher:
    def __init__(self, key):
        self.key = get_key(key)
        self.cipher = Fernet(self.key)
        
    def encrypt(self, data):
        encrypted_data = self.cipher.encrypt(data.encode())
        return encrypted_data.hex()
        
    def decrypt(self, data):
        decrypted_data = self.cipher.decrypt(bytes.fromhex(data))
        return decrypted_data.decode()