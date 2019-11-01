# Transposition Cipher Encryption

def main():
    myMessage = 'Common sense is not so common'
    myKey = 8

    ciphertext = encryptMessage(myKey, myMessage)

    # Print the encrypted string in ciphertext to the screen, with
    # a '|' after it to indicate the end of the message
    print(ciphertext + '|')

def encryptMessage(key, message):
    # Each string in ciphertext represents a column in the grid
    ciphertext = [''] * key

    # Loop through each column in ciphertext
    for column in range(key):
        currentIndex = column

        # Keep looping until currentIndex goes past the message length:
        while currentIndex < len(message):
            # Place the character at currentIndex in message at the end
            # of the current column in the ciphertext list
            ciphertext[column] += message[currentIndex]

            # Move currentIndex over
            currentIndex += key

    # Convert the ciphertext list into a single string value and return
    return ''.join(ciphertext)

# If the transpositionEncrypt.py is run (instead of imported as a module)
# call the main() function
if __name__ == '__main__':
    main()