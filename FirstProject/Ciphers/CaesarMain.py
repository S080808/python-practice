import os
from CaesarCipher.CaesarRequests import CaesarRequests

class CaesarMenu:
    def caesar_menu(self, request, input_file, key_txt, output_file):
        """
            Process the Caesar cipher operation based on the user's request.

            Parameters:\n
            - request (str): The operation requested by the user. Can be 'en' for encrypt or 'de' for decrypt or 'br' for break.
            - input_file (str): The name of the file containing the text to be encrypted or decrypted.
            - key_file (str): The name of the file containing the encryption key.
            - output_file (str): The name of the file where the encrypted or decrypted text will be saved.

            Returns:
            - None
            """
        rqs = CaesarRequests()

        if request in ['de', 'en']: # if request is encrypt or decrypt
            if not os.path.isfile(key_txt):
                print("Key file does not exist!")
                return
            with open(key_txt, 'r', encoding='utf-8') as file:
                key = file.read()

            if key[:3] not in ['rot', 'ROT'] or not key[3:].isnumeric():
                print("Wrong key format. Please try again.")
                return
            if request == 'en': # encrypt
                rqs.encrypting_request(input_file, key, output_file)
            elif request == 'de': # decrypt
                rqs.decrypting_request(input_file, key, output_file)
        elif request == 'br':
            if not os.path.isfile(key_txt):
                print("Key file does not exist!")
                return
            rqs = CaesarRequests()
            rqs.breaking_request(input_file, output_file)
        else:
            print("Invalid request!")