alph_size = 26 # English alphabet size
class Caesar:
    def encrypt(self, text, shift):
        """
         Encrypts the given text using the Caesar cipher with the specified shift.

         This method applies the Caesar cipher encryption algorithm to the input text.
         Each alphabetic character in the text is shifted by the number of positions
         specified by the 'shift' parameter. The case of the alphabetic characters is
         preserved, and non-alphabetic characters are left unchanged.

         Parameters:\n
         - text (str): The text that needs to be encrypted.
         - shift (int): The number of positions each alphabetic character in the text
                        will be shifted. A positive shift value shifts characters to
                        the right in the alphabet, while a negative value shifts to the left.

         Returns:\n
         - str: The encrypted text as a result of applying the Caesar cipher.

         Note:\n
         - The function preserves the case of the alphabetic characters in the input text.
         - Non-alphabetic characters are not encrypted but are included in the output
           text in their original form.

         Example usage:\n
         >>> cipher = CaesarCipher()
         >>> cipher.encrypt('Hello World', 3)
         # Returns 'Khoor Zruog' after shifting each character in 'Hello World' by 3 positions.
         """
        output_text = ''
        for symbol in text:
            if symbol.isalpha():
                min_char = 65 if symbol.isupper() else 97
                output_text += \
                    chr((ord(symbol) - min_char + shift) %
                        alph_size + min_char)
            else:
                output_text += symbol
        return output_text

    def breaking(self, text, letter):
        """
            Breaks the Caesar cipher using frequency analysis.

            This method attempts to break the Caesar cipher by identifying the most
            frequently occurring character in the ciphertext and assuming it represents
            a particular letter in the plaintext (commonly 'e' in English). It calculates
            the shift used to encrypt the original text and writes the key to 'key.txt'.
            It then decrypts the text using the identified shift.

            Parameters:\n
            - text (str): The ciphertext that needs to be decrypted.
            - letter (str): The letter that is assumed to be the most frequent in the
                            plaintext. This is typically the letter 'e' for English text.

            Returns:\n
            - str: The decrypted text after applying frequency analysis to break the cipher.

            Side effects:\n
            - Writes the identified key to 'key.txt' in the format 'ROT{shift}'.

            Note:\n
            - The function assumes that the input text is in lowercase and that spaces
              are not counted in the frequency analysis.
            - The function only considers alphabetic characters and ignores all other
              types of characters.

            Example usage:\n
            >>> cipher = CaesarCipher()
            >>> cipher.breaking('lqkp ogfke', 'e')
            # Assuming 'e' is the most frequent letter, it identifies the shift and
            # returns the decrypted text. It also writes 'ROT5' to 'key.txt'.
        """
        symbols = {}
        most_frequent_counter = 0
        most_frequent_symbol = '0'
        for symbol in text:
            if symbol == ' ':
                continue
            if symbol in symbols:
                symbols[symbol] += 1
            else:
                symbols[symbol] = 1
            if symbols[symbol] > most_frequent_counter:
                most_frequent_counter = symbols[symbol]
                most_frequent_symbol = symbol
        delta = ord(most_frequent_symbol) - ord(letter)

        with open("key.txt", 'w', encoding='utf-8') as file:
            file.write(f"ROT{delta % alph_size}")
        return self.encrypt(text, -delta)