# Transposition Cipher Test

import random, sys, transpositionEncrypt, transpositionDecrypt

def main():
    random.seed(42) # Set a random seed

    for i in range(20):
        # Generate random message to test with random length
        message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * random.randint(4, 40)

        # Convert message into list and shuffle then back to string
        message = list(message)
        random.shuffle(message)
        message = ''.join(message)

        print(f'Test #{i+1}: "{message[:50]}..."')

        # Check all possible keys for each message
        for key in range(1, int(len(message)/2)):
            encrypted = transpositionEncrypt.encryptMessage(key, message)
            decrypted = transpositionDecrypt.decryptMessage(key, encrypted)

            # If decryption doesn't match, display error message and quit
            if message != decrypted:
                print(f'Mismatch with key: {key} and message: {message}')
                print(f'Decrypted as: {decrypted}')
                sys.exit()

    print('Transposition cipher test passed.')

# If transpositionTest.py is run (instead of imported as module
# call the 'main()' function
if __name__ == '__main__':
    main()