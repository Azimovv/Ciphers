# Caesar Cipher
from random import randint

def crypter(message, key, encOrdec):
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.`~@#$%^&*()_+-=[]{}|;:<>,/'
    crypted = ''
    key = int(key)

    # Create random key if no key is provided for encryption
    if key == 0 and encOrdec == 1:
        key = randint(1, len(symbols))

    # Brute force method for decryption
    elif key == 0 and encOrdec == 3:
        for i in range(len(symbols)):
            for character in message:
                new_index = symbols.find(character) - i
                if new_index < 0:
                    new_index = new_index + len(symbols)
                crypted += symbols[new_index]
            print(f"Decrypted message: '{crypted}', with key {i}")
            crypted = ''

    # Parse message and create encryption or decrypt using key
    else:
        for character in message:
            if encOrdec == 1:
                new_index = symbols.find(character) + key
            else:
                new_index = symbols.find(character) - key

            # Handling wraparound
            if new_index >= len(symbols):
                new_index = new_index - len(symbols)
            elif new_index < 0:
                new_index = new_index + len(symbols)

            crypted += symbols[new_index]

        if encOrdec == 1:
            print(f"Your encrypted message is: '{crypted}' with a key of {key}")
        else:
            print(f"Your decrypted message is: '{crypted}' with a key of {key}")


choice = input("Would you like to encrypt a message or decrypt a message?"
               "(Enter encrypt or decrypt): ")

if choice == 'encrypt':
    encOrdec = 1
    message = input("Enter a message to be encrypted: ")
    key = input("Enter a key for the encryption (Enter 0 for random key): ")
    crypter(message, key, encOrdec)

elif choice == 'decrypt':
    message = input("Enter a message to be decrypted: ")
    key = input("Enter the key for the decryption "
                "(Enter 0 for brute force decryption): ")
    if key == '0':
        encOrdec = 3
    else:
        encOrdec = 0
    crypter(message, key, encOrdec)

else:
    print("Please enter either 'encrypt' or 'decrypt'")
