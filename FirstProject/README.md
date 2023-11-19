# Classic Cipher Suite

This project is a command-line utility for encrypting and decrypting text using three ciphers: Caesar, Vigenère, and Vernam. Additionally, it includes a Caesar cipher breaker using frequency analysis.

## Features

- **Caesar Cipher**: Encrypt or decrypt text, preserving letter case. The program can also break the cipher without a key using frequency analysis.
- **Vigenère Cipher**: Encrypt or decrypt text using a provided key. The program can also generate a key if none is provided for encryption.
- **Vernam Cipher**: Encrypt text with an automatically generated key and decrypt text with a key that matches the length of the input text.

## Usage
Run the program from the command line using the following pattern:

python ClassicCipherSuite.py <cipher> <mode> <input_file_name> <key_file_name> <output_file_name>


Where:
- `<cipher>` is one of `csr` (Caesar), `vgn` (Vigenere), or `vrn` (Vernam).
- `<mode>` is one of `en` (encrypt), `de` (decrypt), or `br` (break - only for Caesar cipher).
- `<input_file_name>` is the name of the file containing the text to be processed.
- `<key_file_name>` is the name of the file containing the key for encryption/decryption. For Caesar cipher breaking, this file will be used to output the found key. For Vigenère encryption, enter `-` to have the program generate a key.
- `<output_file_name>` is the name of the file where the processed text will be saved.

### Examples

#### Encrypt with Caesar cipher:
python main.py csr en input.txt ROT13 output.txt

#### Decrypt with Vigènere cipher (using a custom key):
python main.py vgn de input.txt key.txt output.txt

#### Encrypt with Vernam cipher (key will be generated):
python main.py vrn en input.txt - output.txt

## Requirements

This project uses Python's standard library. No external dependencies are required.

## Notes

- The Caesar cipher maintains the case of the letters during encryption and decryption.
- The Vigenère cipher requires a key for decryption. For encryption, the program can generate a key if not provided.
- The Vernam cipher's key for decryption must match the length of the input text.