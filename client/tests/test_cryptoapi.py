import unittest
import os
import sys
from pathlib import Path

from src.cryptoapi import cmd_encrypt_decrypt, cmd_hashify

#TODO: configure output path, as of now pick cwd, license.txt file.
PROJECT_PATH = os.getcwd() #run test from top folder.
OUT_PATH = os.path.join(PROJECT_PATH, "output" )
Path(OUT_PATH).mkdir(parents=True, exist_ok=True)
TEST_TXT_FILE = os.path.join(OUT_PATH,"tests", "LICENSE.txt")
print(TEST_TXT_FILE)

TEST_TXT_FILE = "LICENSE.txt"

class TestCLI(unittest.TestCase):

    def test_cmd_encrypt_decrypt(self):
        # 1. run the cmd func.
        cmd_encrypt_decrypt(TEST_TXT_FILE, 'encrypt', 'localhost', 5000)
        # test if encrypted file is downloaded.
        downloaded_file_encrypted = Path(TEST_TXT_FILE+".encrypt")
        self.assertTrue(downloaded_file_encrypted.is_file())

        # 2. test server decryption
        cmd_encrypt_decrypt(downloaded_file_encrypted.name, 'decrypt', 'localhost', 5000)
        downloaded_file_decrypted = Path(TEST_TXT_FILE+".encrypt"+".decrypt") #name after downloading
        self.assertTrue(downloaded_file_decrypted.is_file())

        # 3. test if file decrypted is same as original file.
        # since it is a small sized file, I can convert it to string and test if equal.

        original_content = None
        decrypted_content = None

        with open(TEST_TXT_FILE) as fd:
            original_content = fd.read()

        with open(downloaded_file_decrypted) as fd:
            decrypted_content = fd.read()
        
        if original_content and decrypted_content:
            self.assertEqual(original_content, decrypted_content)
    
        else:
            raise ValueError("Original content or decrypted content is none.")

        # clean up
        Path.unlink(downloaded_file_encrypted)
        Path.unlink(downloaded_file_decrypted)

    def test_hashify(self):
        # Test if password is more than 20 chars, throw error.
        res = cmd_hashify("ThisIsAnExampleOfLongPassword.ItsPracticalToUse")
        self.assertEqual(res.json()['message'],'Password must be less than 20 chars.')

    #TODO: implement commands and mock requests when you hit actual API. For now, 