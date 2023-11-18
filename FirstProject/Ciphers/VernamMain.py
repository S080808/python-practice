from VernamCipher.VernamRequests import VernamRequests

class VernamMenu:
    def vernam_menu(self, request, input_file, key_file, output_file):
        """
            Process the Vernam cipher operation based on the user's request.

            Parameters:\n
            - request (str): The operation requested by the user. Can be 'en' for encrypt or 'de' for decrypt.
            - input_file (str): The name of the file containing the text to be encrypted or decrypted.
            - key_file (str): The name of the file containing the encryption key. For encryption, program will write generated key into the file.
            - output_file (str): The name of the file where the encrypted or decrypted text will be saved.

            Returns:
            - None
        """
        rqs = VernamRequests()

        if request == 'en': # encrypt
            rqs.first_request(input_file, key_file, output_file)
        if request == 'de': # decrypt
            rqs.second_request(input_file, key_file, output_file)