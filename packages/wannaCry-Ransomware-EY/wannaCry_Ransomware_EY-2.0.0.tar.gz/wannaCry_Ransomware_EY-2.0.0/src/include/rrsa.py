import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA


class Rsa:
    def __init__(self, key: str):
        self.key = RSA.import_key(key)
        self.rsa_cipher = PKCS1_OAEP.new(self.key)

    def encrypt(self, fp: str):
        try:
            aes_key = get_random_bytes(32)
            aes_cipher = AES.new(aes_key, AES.MODE_EAX)
            encrypted_aes_key = self.rsa_cipher.encrypt(aes_key)

            with open(fp, 'rb') as f:
                data = f.read()

            ciphertext, tag = aes_cipher.encrypt_and_digest(data)

            encrypted_fp = fp + '.enc'  # set encrypted file name and path, example: usr/tmp/file.exe > usr/tmp/file.exe.enc
            # create encrypted file and write to it relevant cipher data including the encrypted AES key
            # NOTE: AES key length after encryption is 256 bytes!
            with open(encrypted_fp, 'wb') as f:
                f.write(encrypted_aes_key)
                f.write(aes_cipher.nonce)
                f.write(tag)
                f.write(ciphertext)
            return encrypted_fp
        except Exception as e:
            print(e)
            return None
