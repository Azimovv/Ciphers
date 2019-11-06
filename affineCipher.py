# Affine Cipher

import sys, cryptomath, random
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def main():
    message = input("Enter a message to encrypt or decrypt: ")
    key = input("Enter a key (leave empty for random key): ")
    mode = input("Enter if you'd like to 'encrypt' or 'decrypt' the message: ")

    if key == '':
        key = getRandomKey()
    key = int(key)
    if mode == 'encrypt':
        translated = encryptMessage(key, message)
    elif mode == 'decrypt':
        translated = decryptMessage(key, message)

    print(f"Key: {key}")
    print(f"{mode.title()}ed text")
    print(translated)

def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)

def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        sys.exit("Cipher is weak if key A is 1. Choose a different key.")
    if keyB == 0 and mode == 'encrypt':
        sys.exit("Cipher is weak if key B is 0. Choose a different key.")
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        sys.exit(f"Key A must be greater than 0 and Key B must be between "
                 f"0 and {len(SYMBOLS) - 1}")
    if cryptomath.gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit(f"Key A {keyA} and the symbol set size {len(SYMBOLS)} are "
                 f"not relatively prime. Choose a different key.")

def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    ciphertext = ''
    for symbol in message:
        if symbol in SYMBOLS:
            # Encrypt symbol
            symbol_index = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symbol_index * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += symbol # Append symbol without encryption
    return ciphertext

def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plaintext = ''
    mod_inverse = cryptomath.findModInverse(keyA, len(SYMBOLS))

    for symbol in message:
        if symbol in SYMBOLS:
            # Decrypt symbol
            symbol_index = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symbol_index - keyB) * mod_inverse % len(SYMBOLS)]
        else:
            plaintext += symbol # Append symbol without decryption
    return plaintext

def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if cryptomath.gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB

# If affineCipher.py is run (instead of imported as a module), call
# the main() function
if __name__ == '__main__':
    main()