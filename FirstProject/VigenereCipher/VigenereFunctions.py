kMinChar = 97 # 'a' in ASCII
kAlphSize = 26 # English alphabet size

class Vigenere:
    def encrypt(self, text, key):
        """
            Encrypts the given text using the Vigenere cipher with the provided key.

            This method applies the Vigenere cipher encryption algorithm to the input text.
            It iterates over each character in the text, shifting it by the corresponding
            character in the key. Non-alphabetic characters are left unchanged. The key is
            repeated or truncated as necessary to match the length of the text.

            Parameters:\n
            - text (str): The text that needs to be encrypted.
            - key (str): The key string used for encryption. The key's length should be equal to text's length.

            Returns:\n
            - str: The encrypted text as a result of applying the Vigenere cipher.

            Note:\n
            - The function assumes that the input text and the key are in lowercase.
            - Non-alphabetic characters in the input text are not encrypted but are
              included in the output text in their original form.

            Example usage:\n
            >>> cipher = Vigenere()
            >>> cipher.encrypt('hello world', key)
            # Returns the encrypted text using the Vigenere cipher with the provided key.
            """
        output_text = ''
        key_index = 0
        for symbol in range(len(text)):
            if text[symbol].isalpha():
                output_text +=\
                    chr((ord(text[symbol]) + ord(key[key_index % len(key)]) -
                         2 * kMinChar) % kAlphSize + kMinChar)
                key_index += 1
            else:
                output_text += text[symbol]
        return output_text

    def decrypt(self, text, key):
        """
            Decrypts the given text using the Vigenere cipher with the provided key.

            This method applies the Vigenere cipher decryption algorithm to the input text.
            It iterates over each character in the text, shifting it by the corresponding
            character in the key. Non-alphabetic characters are left unchanged.

            Parameters:\n
            - text (str): The text that needs to be decrypted.
            - key (str): The key string used for encryption. The key's length should be equal to text's length.

            Returns:\n
            - str: The decrypted text as a result of applying the Vigenere cipher.

            Note:\n
            - The function assumes that the input text and the key are in lowercase.
            - Non-alphabetic characters in the input text are not decrypted but are
              included in the output text in their original form.

            Example usage:\n
            >>> cipher = Vigenere()
            >>> cipher.decrypt('hello world', key)
            # Returns the decrypted text using the Vigenere cipher with the provided key.
            """
        output_text = ''
        key_index = 0
        for symbol in range(len(text)):
            if text[symbol].isalpha():
                output_text +=\
                    chr((ord(text[symbol]) - ord(key[key_index % len(key)])) % kAlphSize + kMinChar)
                key_index += 1
            else:
                output_text += text[symbol]
        return output_text
