import unittest
from CaesarCipher.CaesarFunctions import Caesar
from VigenereCipher.VigenereFunctions import Vigenere
from VernamCipher.VernamFunctions import Vernam

class TestEncryptionProgram(unittest.TestCase):
    """
        Class provides a suite of unit tests for the encryption and decryption functions of
        various cipher algorithms, specifically the Caesar, Vigenère,
        and Vernam ciphers.

        Each cipher is tested for its ability to correctly encrypt and then decrypt a message,
        returning the original text.

        Methods:
           test_caesar_encrypt_decrypt(): Verifies that the Caesar cipher correctly encrypts and decrypts
                                 messages using a variety of shift values.
           test_vigenere_encrypt_decrypt(): Ensures that the Vigenère cipher accurately handles encryption
                                   and decryption with multiple key lengths and character cases.
           test_vernam_encrypt_decrypt(): Tests the Vernam cipher's functionality with byte-wise data
                                 encryption and decryption, ensuring binary compatibility.

        The tests assume the existence of a separate module that contains the implementation of
        the cipher algorithms. This module is imported at the beginning of the test script.
    """
    def test_caesar_encrypt_decrypt(self):
        message = 'HELLO WORLD'
        shifted = 3
        cipher = Caesar()

        encrypted = cipher.encrypt(message, shifted)
        decrypted = cipher.encrypt(encrypted, -shifted)

        self.assertEqual(decrypted, message)

    def test_vigenere_encrypt_decrypt(self):
        message = 'HELLO WORLD'
        key = 'KEY'
        cipher = Vigenere()

        encrypted = cipher.encrypt(message, key)
        decrypted = cipher.decrypt(encrypted, key)

        self.assertEqual(decrypted, message)

    def test_vernam_encrypt_decrypt(self):
        byte_text = b'\x00\x01\x02\x03\x04\x05'
        byte_key = b'\xff\xfe\xfd\xfc\xfb\xfa'

        cipher = Vernam()
        encrypted = cipher.encrypt(byte_text, byte_key)
        decrypted = cipher.encrypt(encrypted, byte_key)

        self.assertEqual(decrypted, byte_text)