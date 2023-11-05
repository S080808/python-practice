import os

def key_generator(size):
    return os.urandom(size)

def first_request(cipher, input_file, key_file, output_file): # encrypt
    """
        Handles the first request for the encryption process. It reads the input file,
        generates a key, writes the key to the key file, encrypts the text, and writes
        the encrypted text to the output file.

        Parameters:\n
        - cipher (Cipher): An instance of the cipher class that will be used for encryption.
        - input_file (str): The path to the file containing the plaintext.
        - key_file (str): The path to the file where the generated key will be saved.
        - output_file (str): The path to the file where the encrypted text will be saved.

        The function checks if the input file exists, reads its content, generates a key
        of equal length to the text, saves the key to the key file, encrypts the text using
        the provided cipher instance, and writes the encrypted data to the output file.

        If the input file does not exist, it prints an error message and returns without
        performing encryption.

        Note:\n
        - The input file is read in binary mode ('rb'), which means the text should be
          in bytes format.
        - The key and output files are written in binary mode ('wb').
        - The key is generated using a separate `key_generator` function, which should be
          defined elsewhere in the code.

        Example usage:\n
        >>> cipher = VernamCipher()
        >>> first_request(cipher, 'plaintext.txt', 'key.txt', 'encrypted.txt')
        # This will encrypt the content of 'plaintext.txt' and save the key to 'key.txt'
        # and the encrypted text to 'encrypted.txt'.
        """
    if not os.path.isfile(input_file):  # if path does not exist
        print("Input file does not exist.")
        return

    with open(input_file, 'rb') as file:
        text = file.read().lower()

    key = key_generator(len(text))

    with open(key_file, 'wb') as file:
        file.write(key)
    print(f"Default key has been saved to {key_file}.")

    with open(output_file, 'wb') as file:
        file.write(cipher.encrypt(text, key))
    print(f"Text has been encrypted and saved to {output_file}.")

def second_request(cipher, input_file, key_file, output_file):
    """
        Handles the second request for the decryption process. It reads the input file and the key file,
        ensures they are of equal length, decrypts the text, and writes the decrypted text to the output file.

        Parameters:\n
        - cipher (Cipher): An instance of the cipher class that will be used for decryption.
        - input_file (str): The path to the file containing the encrypted data.
        - key_file (str): The path to the file where the key is stored.
        - output_file (str): The path to the file where the decrypted text will be saved.

        The function checks if the input and key files exist and reads their contents. It then verifies that
        the key and the encrypted data are of the same length. If they are, it proceeds to decrypt the text
        using the provided cipher instance and writes the decrypted data to the output file. If the key and
        encrypted data lengths do not match, it prints an error message and returns without performing decryption.

        Note:\n
        - The input and key files are read in binary mode ('rb'), which means the text and key should be
          in bytes format.
        - The output file is written in binary mode ('wb').

        Example usage:\n
        >>> cipher = VernamCipher()
        >>> second_request(cipher, 'encrypted.txt', 'key.txt', 'decrypted.txt')
        # This will decrypt the content of 'encrypted.txt' using the key from 'key.txt'
        # and save the decrypted text to 'decrypted.txt'.
        """
    if not os.path.isfile(input_file):  # if path does not exist
        print("Input file does not exist.")
        return

    with open(input_file, 'rb') as file:
        text = file.read()

    if not os.path.isfile(key_file):  # if path does not exist
        print("Key file does not exist.")
        return
    with open(key_file, 'rb') as file:
        key = file.read()

    if len(key) != len(text):
        print("Key and encrypted data must be of the same length!")
        return

    with open(output_file, 'wb') as file:
        file.write(cipher.encrypt(text, key))
    print(f"Text has been decrypted and saved to {output_file}.")

