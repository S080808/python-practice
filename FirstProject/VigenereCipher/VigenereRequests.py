import os
import random

kMinChar = 97 # 'a' in ASCII
kAlphSize = 26 # English alphabet size

def key_generator(size):
    '''
    Generates key with random english alphabet letters.
    Parameters:\n
    - size: An actual length of needed key.
    Returns:\n
    - Generated key.
    Example usage:\n
        >>> key = VigenereCipher(10)
        # This will generate a key with random english alphabet letters of the length of 10.
    '''
    key = ''
    for i in range(size):
        key += chr(kMinChar + random.randint(0, kAlphSize - 1))
    return key

def first_request(cipher, input_file, key_file, output_file): # encrypt
    """
        Processes the encryption request for a given text file using the specified cipher. If a key file is not provided,
        a default key is generated and saved.

        Parameters:\n
        - cipher (Cipher): An instance of the cipher class that will be used for encryption.
        - input_file (str): The path to the file containing the text.
        - key_file (str): The path to the file containing the key or '-' to indicate that a default key should be generated.
        - output_file (str): The path to the file where the encrypted text will be saved.

        The function checks if the input file exists and reads its content. If the key file is specified as '-', a new key
        is generated using the key_generator function and saved to 'default_key.txt'. Otherwise, it checks if the key file
        exists and reads the key from it. The text is encrypted using the provided key and the cipher, and the encrypted text
        is written to the output file in UTF-8 encoding. If the input file or key file does not exist, it prints an error
        message and returns.

        Note:\n
        - The input and output files are handled in text mode, and the text is expected to be in lowercase for accurate
          encryption.
        - The function assumes that the key should be as long as the text for encryption. If the key is shorter, it may
          be repeated or handled according to the cipher's specifications.

        Example usage:\n
        >>> cipher = VigenereCipher()
        >>> first_request(cipher, 'plaintext.txt', '-', 'encrypted.txt')
        # This will encrypt 'plaintext.txt' using a generated key, save the key to 'default_key.txt',
        # and save the encrypted text to 'encrypted.txt'.
    """
    if not os.path.isfile(input_file):  # if path does not exist
        print("Input file does not exist.")
        return
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    if key_file == '-':
        key = key_generator(len(text))
        key_file = "default_key.txt"
        with open(key_file, 'w', encoding='utf-8') as file:
            file.write(key)
        print(f"Default key has been saved to {key_file}.")
    else:
        if not os.path.isfile(key_file):  # if path does not exist
            print("Key file does not exist.")
            return
        with open(key_file, 'r', encoding='utf-8') as file:
            key = file.read().lower()

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cipher.encrypt(text, key))
    print(f"Text has been encrypted and saved to {output_file}.")

def second_request(cipher, input_file, key_file, output_file): # decrypt
    """
        Processes the decryption request for a given text file using the specified cipher.

        Parameters:\n
        - cipher (Cipher): An instance of the cipher class that has been used for encryption.
        - input_file (str): The path to the file containing the text.
        - key_file (str): The path to the file containing the key.
        - output_file (str): The path to the file where the encrypted text will be saved.

        The function checks if the input file exists and reads its content. Function checks if the key file
        exists and reads the key from it. The text is decrypted using the provided key and the cipher, and the decrypted text
        is written to the output file in UTF-8 encoding. If the input file or key file does not exist, it prints an error
        message and returns.

        Note:\n
        - The input and output files are handled in text mode, and the text is expected to be in lowercase for accurate
          encryption.
        - The function assumes that the key should be as long as the text for encryption. If the key is shorter, it may
          be repeated or handled according to the cipher's specifications.

        Example usage:\n
        >>> cipher = VigenereCipher()
        >>> first_request(cipher, 'plaintext.txt', '-', 'encrypted.txt')
        # This will encrypt 'plaintext.txt' using a generated key, save the key to 'default_key.txt',
        # and save the encrypted text to 'encrypted.txt'.
    """
    if not os.path.isfile(input_file):  # if path does not exist
        print("Input file does not exist.")
        return
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    if not os.path.isfile(key_file):  # if path does not exist
        print("Key file does not exist.")
        return
    with open(key_file, 'r', encoding='utf-8') as file:
        key = file.read()

    if len(key) != len(text):
        if len(key) > len(text):
            key = key[:len(text)]
        else:
            key = (key * (len(text) // len(key) + 1))[:len(text)]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cipher.decrypt(text, key))
    print(f"Text has been decrypted and saved to {output_file}.")
