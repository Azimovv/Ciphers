# Simple Substitution Cipher

import sys, random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    message = input("Enter a message for encryption or decryption: ")
    key = input("Enter a key (leave empty for random key): ")
    mode = input("Enter if you would like to 'encrypt' or 'decrypt': ")

    if key == '':
        key = getRandomKey()
    if not keyIsValid(key):
        sys.exit("There is an error in the key or symbol set.")
    if mode == 'encrypt':
        translated = encryptMessage(key, message)
    elif mode == 'decrypt':
        translated = decryptMessage(key, message)
    print(f"Using key: {key}")
    print(f"The {mode}ed messsage is: ")
    print(translated)

def keyIsValid(key):
    key_list = list(key)
    letters_list = list(LETTERS)
    key_list.sort()
    letters_list.sort()

    return key_list == letters_list

def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')

def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')

def translateMessage(key, message, mode):
    translated = ''
    charsA = LETTERS
    charsB = key
    if mode == 'decrypt':
        # decrypting will use same code as encrypting but
        # where the key and LETTERS strings are used are swapped
        charsA, charsB = charsB, charsA

    # Loop through each symbol in the message
    for symbol in message:
        if symbol.upper() in charsA:
            # Encrypt/decrypt symbol
            sym_index = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[sym_index].upper()
            else:
                translated += charsB[sym_index].lower()
        else:
            # Symbol is not in LETTERS, add it
            translated += symbol

    return translated

def getRandomKey():
    key = list(LETTERS)
    random.shuffle(key)
    return ''.join(key)


if __name__ == '__main__':
    main()