from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

class AESCipher:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()  # Ensure the key is hashed to 32 bytes
        self.cipher = AES.new(self.key, AES.MODE_CBC)

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()  # Ensure the string is converted to bytes before encryption
        padded_data = pad(data, AES.block_size)
        return self.cipher.encrypt(padded_data)

    def decrypt(self, data):
        if isinstance(data, str):
            data = data.encode()  # Ensure the string is converted to bytes before decryption
        decrypted_data = unpad(self.cipher.decrypt(data), AES.block_size)
        return decrypted_data
