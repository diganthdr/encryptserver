from asyncio.log import logger
from Crypto.Cipher import AES

from encdec.crypt import Crypt
from settings import SECRET_KEY_AES, logger

# to add new algo, 
# 1. inherit from Crypt (at the moment it does not add any value but infuture it can), make encrypt, decrypt funcs 
# 2. create a function like below
# def <your algo name>(<operation type>): operation type is encrypt or decrypt

class CryptAES(Crypt):
    def __init__(self, mode=AES.MODE_CFB):
        """ constructor takes mode as input for AES, default is CFB """
        self.key = self.get_key()
        self.mode = mode
        super().__init__()
    
    def encrypt(self, message):
        obj = AES.new(self.key, self.mode, 'This is an IV456')
        ciphertext = obj.encrypt(message)
        return ciphertext

    def decrypt(self, message):
        obj = AES.new(self.key, self.mode, 'This is an IV456')
        message = obj.decrypt(message)
        return message
    
    def get_key(self):
       return SECRET_KEY_AES


# driver code based on operation
def aes(filename, operation):
    A = CryptAES()
    result = None

    logger.debug(f"AES algo on file: {filename}, operation: {operation}")
    if operation == 'encrypt':
        with open(filename, 'r') as fd:
            message = fd.read()
            result = A.encrypt(message)
    elif operation == 'decrypt':
        with open(filename, 'rb') as fd:
            message = fd.read()
            result = A.decrypt(message)
    else:
        raise ValueError(f"Unknown operation: {operation}")

    return result