from VigenereCipher.VigenereRequests import VigenereRequests

class VigenereMenu():
    def vigenere_menu(self, request, input_file, key_file, output_file):
        """
            Process the Vigenere cipher operation based on the user's request.

            Parameters:\n
            - request (str): The operation requested by the user. Can be 'en' for encrypt or 'de' for decrypt.
            - input_file (str): The name of the file containing the text to be encrypted or decrypted.
            - key_file (str): The name of the file containing the encryption key. For encryption, this can also be the destination file for a generated key.
            - output_file (str): The name of the file where the encrypted or decrypted text will be saved.

            Returns:
            - None
        """
        rqs = VigenereRequests()

        if request == 'en': # encrypt
            rqs.first_request(input_file, key_file, output_file)
        elif request == 'de':
            rqs.second_request(input_file, key_file, output_file)
        else:
            print("Invalid request, try again!")