import unittest
from CaesarCipher.CaesarFunctions import CaesarFunctions
from VigenereCipher.VigenereFunctions import VigenereFunctions
from VernamCipher.VernamFunctions import VernamFunctions

class TestEncryptionProgram(unittest.TestCase):
    def test_caesar_encrypt_decrypt(self):
        message = 'hello world'
        shifted = 3
        cipher = CaesarFunctions()

        encrypted = cipher.encrypt(message, shifted)
        decrypted = cipher.encrypt(encrypted, -shifted)

        self.assertEqual(decrypted, message)

    def test_caesar_breaking(self):
        message = "Ellen's collection of books is extensive, featuring works from esteemed authors. She believes that reading not only entertains but also educates and enlightens."
        shifted = 3;
        cipher = CaesarFunctions()

        encrypted = cipher.encrypt(message, shifted)
        decrypted = cipher.breaking(encrypted, 'e')

        self.assertEqual(message, decrypted)


    def test_vigenere_encrypt_decrypt(self):
        message = 'hello world'
        key = 'key'
        cipher = VigenereFunctions()

        encrypted = cipher.encrypt(message, key)
        decrypted = cipher.decrypt(encrypted, key)

        self.assertEqual(decrypted, message)

    def test_vernam_encrypt_decrypt(self):
        byte_text = b'\x00\x01\x02\x03\x04\x05'
        byte_key = b'\xff\xfe\xfd\xfc\xfb\xfa'

        cipher = VernamFunctions()
        encrypted = cipher.encrypt(byte_text, byte_key)
        decrypted = cipher.encrypt(encrypted, byte_key)

        self.assertEqual(decrypted, byte_text)