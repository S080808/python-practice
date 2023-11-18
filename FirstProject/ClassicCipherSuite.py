from Ciphers.VigenereMain import VigenereMenu
from Ciphers.CaesarMain import CaesarMenu
from Ciphers.VernamMain import VernamMenu
from unit_tests import TestEncryptionProgram
import sys
def main_mode():
    if (len(sys.argv) != 6):
        print("Invalid input, try again!")
        return
    mode, request, input_file, key_file, output_fyle =\
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

    # unit tests were used in development stage to check if functions were working correctly
    unit_tests = TestEncryptionProgram()
    unit_tests.test_caesar_encrypt_decrypt()
    unit_tests.test_vernam_encrypt_decrypt()
    unit_tests.test_vernam_encrypt_decrypt()


    if mode == 'csr':
        menu = CaesarMenu()
        menu.caesar_menu(request, input_file, key_file, output_fyle)
    elif mode == 'vgn':
        menu = VigenereMenu()
        menu.vigenere_menu(request, input_file, key_file, output_fyle)
    elif mode == 'vrn':
        menu = VernamMenu()
        menu.vernam_menu(request, input_file, key_file, output_fyle)
    else:
        print("Invalid input, try again!")

if __name__ == "__main__":
    main_mode()