
import unittest
from src.generatehash import generate_hash

class TestStringMethods(unittest.TestCase):

    def test_generate_hash(self):
        # tests if password is hashed and verifies if same hash is generated everytime.
        test_passwords = ["test@123", "J10d4e%M3J46", "S8ze7LP9x!38", "#a2xT4V03957", 
            r"ATU02eElhHVa%3s^nK99x0", "#l@$ak#.lk;0@P",
            "zaq1^*(", "zaq1&*()", "zaq1*()_", "zaq1()+_", "zaq1)+|",
]
        validation_dict = {} 
        # generate hashes in first pass
        for password in test_passwords:
            validation_dict[password] = generate_hash(password)
        
        # generate again and verify if it is same as before
        for password in test_passwords:
            self.assertEqual( generate_hash(password), validation_dict[password])
        


        