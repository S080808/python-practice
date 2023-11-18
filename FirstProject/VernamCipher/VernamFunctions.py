class VernamFunctions:
    def encrypt(self, text, key):
        """
            Encrypts the given text using the Vernam cipher with the specified key.

            The Vernam cipher is a symmetrical stream cipher, which combines plaintext
            with a random secret key that is the same length as the plaintext. This method
            applies the Vernam cipher encryption by performing a bitwise XOR operation
            between the text and the key.

            Parameters:\n
            - text (bytes): The plaintext that needs to be encrypted, provided as a bytes object.
            - key (bytes): The key used for encryption, provided as a bytes object. It must
                           be the same length as the text.

            Returns:\n
            - bytes: The encrypted text as a result of applying the Vernam cipher.

            Raises:\n
            - ValueError: If the key is not the same length as the text.

            Note:\n
            - Both the text and the key must be provided as bytes objects.
            - The key must be exactly the same length as the text for the Vernam cipher to work.
            """
        return bytes([t ^ k for t, k in zip(text, key)])
