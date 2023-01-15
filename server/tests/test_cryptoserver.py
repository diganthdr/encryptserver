import unittest
from encdec.algos.aes import CryptAES

class TestEncryptionDecryption(unittest.TestCase):

    def test_aes_encryption(self):
        A = CryptAES()
        encrypted_text = A.encrypt("Woven planet")
        print(encrypted_text)
        exptected_text = b'\xd2\t\xd7\xa2\xe2!\xcaa_\xea*n' # This needs to be changed if you changed the key. 
        self.assertEqual(exptected_text, encrypted_text)
    
    def test_aes_decryption(self):
        A = CryptAES()
        encrypted_text = b'\xd2\t\xd7\xa2\xe2!\xcaa_\xea*n' # This needs to be changed if you changed the key. 
        decrypted_text = A.decrypt(encrypted_text)
        self.assertEqual(decrypted_text, b'Woven planet')

    def test_encryption_decryption(self):
        A = CryptAES()
        txt = "This is a long story. Let me cut is short..."
        e_txt = A.encrypt(txt)
        d_txt = A.decrypt(e_txt)
        self.assertEqual(txt, str(d_txt, 'UTF-8'))

    # CLI TESTS:
    # Test one char file
    # Test large file, if the file is getting uploaded and processed.
    # Test same filename with different content, files are stored in same dir, this ensures uniqueness
    # Test binary file, it should not be supported at the moment. (security issues)
    # Create multiple upload requests in a loop, throttle the API. (about 10000 times?)


if __name__ == '__main__':
    unittest.main()
