# Vigenere Cipher (Polyalphabetic Substitution Cipher)

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    message = input("Enter a message to encrypt/decrypt: ")
    key = input("Enter a key (alphabetic): ")
    mode = input("Enter if you'd like to 'encrypt' or 'decrypt': ")

    if mode == 'encrypt':
        translated = encrypt_message(key, message)
    elif mode == 'decrypt':
        translated = decrypt_message(key, message)

    print(f"{mode.title()}ed message: ")
    print(translated)

def encrypt_message(key, message):
    return translate_message(key, message, 'encrypt')

def decrypt_message(key, message):
    return translate_message(key, message, 'decrypt')

def translate_message(key, message, mode):
    translated = []  # Stores encrypted/decrypted message string

    key_index = 0
    key = key.upper()

    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            # -1 indicates symbol was not found
            if mode == 'encrypt':
                num += LETTERS.find(key[key_index])  # Add when encrypting
            elif mode == 'decrypt':
                num -= LETTERS.find(key[key_index])  # Subtract when decrypting

            num %= len(LETTERS)  # Handle wraparound

            # Add the encrypted/decrypted symbol to end of translated
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            key_index += 1  # Move to next letter in key
            if key_index == len(key):
                key_index = 0

        else:
            # Append symbol without encrypting/decrypting
            translated.append(symbol)

    return ''.join(translated)

# If vigenereCipher.py is run (instead of imported as module) call
# main() function
if __name__ == '__main__':
    main()