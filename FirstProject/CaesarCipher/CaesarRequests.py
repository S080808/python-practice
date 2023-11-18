from .CaesarFunctions import CaesarFunctions
import os

class CaesarRequests:
    def encrypting_request(self, input_file, key, output_file): # encrypt
        """
            Processes the initial request for encryption. It reads the input file, encrypts the content using the provided key,
            and writes the encrypted text to the output file.

            Parameters:\n
            - cipher (Cipher): An instance of the cipher class that will be used for encryption.
            - input_file (str): The path to the file containing the plaintext data.
            - key (str): The encryption key, expected to be in the format 'ROT<number>'.
            - output_file (str): The path to the file where the encrypted text will be saved.

            The function checks if the input file exists and reads its content. It then encrypts the text using the provided key
            after extracting the numerical part from the key's 'ROT<number>' format. The encrypted text is written to the output file
            in UTF-8 encoding. If the input file does not exist, it prints an error message and returns.

            Note:\n
            - The input and output files are handled in text mode, which means the text is expected to be in string format.
            - The key is expected to be a string starting with 'ROT' followed by a number which represents the shift for the cipher.
            """
        cipher = CaesarFunctions()
        if not os.path.isfile(input_file):
            print("Input file does not exist!")
            return
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(cipher.encrypt(text, int(key[3:])))
        print(f"Text has been encrypted and saved to {output_file}.")

    def decrypting_request(self, input_file, key, output_file):
        """
            Processes the initial request for decryption. It reads the input file, decrypts the content using the provided key,
            and writes the decrypted text to the output file.

            Parameters:\n
            - cipher (Cipher): An instance of the cipher class that will be used for encryption.
            - input_file (str): The path to the file containing the plaintext data.
            - key (str): The encryption key, expected to be in the format 'ROT<number>'.
            - output_file (str): The path to the file where the encrypted text will be saved.

            The function checks if the input file exists and reads its content. It then decrypts the text using the provided key
            after extracting the numerical part from the key's 'ROT<number>' format. The decrypted text is written to the output file
            in UTF-8 encoding. If the input file does not exist, it prints an error message and returns.

            Note:\n
            - The input and output files are handled in text mode, which means the text is expected to be in string format.
            - The key is expected to be a string starting with 'ROT' followed by a number which represents the shift for the cipher.
        """
        cipher = CaesarFunctions()
        if not os.path.isfile(input_file):
            print("Input file does not exist!")
            return
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(cipher.encrypt(text, -int(key[3:])))
        print(f"Text has been decrypted and saved to {output_file}.")

    def breaking_request(self, input_file, output_file):
        """
            Handles the request to break the cipher. It reads the input file, attempts to break the cipher
            using frequency analysis, and writes the decrypted text to the output file.

            Parameters:\n
            - cipher (Cipher): An instance of the cipher class that will be used for breaking the encryption.
            - input_file (str): The path to the file containing the encrypted text.
            - output_file (str): The path to the file where the decrypted text will be saved.

            The function checks if the input file exists and reads its content. It then attempts to break the cipher by assuming
            'e' is the most frequent letter in the text (which is a common assumption in English). The decrypted text is written
            to the output file in UTF-8 encoding. The key determined by the breaking process is saved to 'key.txt'. If the input
            file does not exist, it prints an error message and returns.

            Note:\n
            - The input and output files are handled in text mode, which means the text is expected to be in string format.
            - The function assumes that the most frequent letter in the text is 'e', which is typical for English language frequency
              analysis but may not hold for texts in other languages or with atypical distributions of letters.
            """
        cipher = CaesarFunctions()
        if not os.path.isfile(input_file):
            print("Input file does not exist!")
            return
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        output_text = cipher.breaking(text, 'e')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output_text)
        print(f"Key has been saved to key.txt.")
        print(f"Text has been broken and saved to {output_file}.")