from VernamCipher.VernamFunctions import Vernam
from VernamCipher.VernamRequests import *

def vernam_menu(request, input_file, key_file, output_file):
    """
        Process the Vernam cipher operation based on the user's request.

        Parameters:\n
        - request (str): The operation requested by the user. Can be 'en' for encrypt or 'de' for decrypt.
        - input_file (str): The name of the file containing the text to be encrypted or decrypted.
        - key_file (str): The name of the file containing the encryption key. For encryption, program will write generated key into the file.
        - output_file (str): The name of the file where the encrypted or decrypted text will be saved.

        Returns:
        - None

        The function does not return any value but prints a message if the request is invalid.
        """
    cipher = Vernam()

    if request == 'en': # encrypt
        first_request(cipher, input_file, key_file, output_file)
    if request == 'de': # decrypt
        second_request(cipher, input_file, key_file, output_file)