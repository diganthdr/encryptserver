from Crypto.Cipher import AES

class Crypt:
    """ This class only handles symmetric encryption """

    def __init__(self):
        """ Algorithm by default is AES in CFB mode """
        pass
    
    def encrypt(self, message):
        """ Takes message for encryption, algorithm by default is AES in CFB mode.
        returns encrypted message """

        raise NotImplementedError("Implement in subclasse")
    
    def get_key(self):
        """ get key from specified location/method
        in: none
        out: string (key) """

        raise NotImplementedError("Implement in subclasse")
