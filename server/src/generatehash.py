import hashlib
import base64


def generate_hash(message, str_encoding='utf-8', hash_algo='sha256'):
    """ generates hash for a given message based on hashlib library. """
    hash_str = base64.b64encode(hashlib.sha256(
        message.encode(str_encoding)).digest())
    # add more algos below in future. TODO: Can be made more modular
    return hash_str


# quick test. more tests are in tests dir
if __name__ == '__main__':
    test_passwords = [
        "test@123",
        "J10d4e%M3J46",
        "S8ze7LP9x!38",
        "#a2xT4V03957",
        r"ATU02eElhHVa%3s^nK99x0"]
    for password in test_passwords:
        generate_hash(password)
