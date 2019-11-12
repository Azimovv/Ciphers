# Public Key Cipher

import sys, math

# Public and private keys for the program were created by the
# makePublicPrivateKeys.py program. Run in same folder as those files

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."

def main():
    # Run test that encrypts or decrypts message to a file
    filename = "encrypted_file.txt"
    mode = "encrypt"  # modes are 'encrypt' and 'decrypt'

    if mode == 'encrypt':
        message = "Journalists belong in the gutter because that is where the " \
                  "ruling classes throw their guilty secrets. Gerald Priestland. " \
                  "The Founding Fathers gave the free press the protection it must " \
                  "have to bare the secrets of government and inform the people. " \
                  "Hugo Black."
        pub_filename = "sunny_p_pubkey.txt"
        print(f"Encrypting and writing to {filename}...")
        encrypted_text = encryptAndWrite(filename, pub_filename, message)

        print("Encrypted text: ")
        print(encrypted_text)

    elif mode == 'decrypt':
        priv_filename = "sunny_p_privkey.txt"
        print(f"Reading from {filename} and decrypting...")
        decrypted_text = readAndDecrypt(filename, priv_filename)

        print("Decrypted text: ")
        print(decrypted_text)

def getBlocks(message, blockSize):
    # Convert string message to list of block ints
    for character in message:
        if character not in SYMBOLS:
            print(f"ERROR: the symbol set does not contain the character {character}.")
            sys.exit()
    block_ints = []
    for blockStart in range(0, len(message), blockSize):
        # Calculate block int for this block of text
        block_int = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            block_int += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
        block_ints.append(block_int)
    return block_ints

def getText(blockInts, messageLength, blockSize):
    # Converts list of block ints to original message string
    # Original message length needed to properly convert last block int
    message = []
    for blockInt in blockInts:
        block_message = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Decode message string for blockSize characters
                char_index = blockInt // (len(SYMBOLS) ** i)
                blockInt %= (len(SYMBOLS) ** i)
                block_message.insert(0, SYMBOLS[char_index])
        message.extend(block_message)
    return ''.join(message)

def encryptMessage(message, key, blockSize):
    # Converts message string to list of block ints
    # then encrypts each block int (pass PUBLIC key to encrypt)
    encrypted_blocks = []
    n, e = key

    for block in getBlocks(message, blockSize):
        # ciphertext = paintext ^ e mod n
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks

def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    # Decrypts list of encrypted block ints into original message
    # Original message length needed to decrypt last block
    # (pass PRIVATE key to decrypt)
    decrypted_blocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decrypted_blocks.append(pow(block, d, n))
    return getText(decrypted_blocks, messageLength, blockSize)

def readKeyFile(keyFilename):
    # Given file that contains a public or private key
    # return key as a (n,e) or (n,d) tuple
    with open(keyFilename, 'r') as fileObj:
        content = fileObj.read()
    key_size, n, EorD = content.split(',')
    return int(key_size), int(n), int(EorD)

def encryptAndWrite(messageFilename, keyFilename, message, blockSize = None):
    # Using key from key file, encrypt the message and save it to the file
    # Returns encrypted message string
    key_size, n, e = readKeyFile(keyFilename)
    if blockSize == None:
        # If blockSize isn't given, set it to largest allowed value
        # determined by key size and symbol set size
        blockSize = int(math.log(2 ** key_size, len(SYMBOLS)))
    # Check key size is large enough for block size
    if not (math.log(2 ** key_size, len(SYMBOLS)) >= blockSize):
        sys.exit("ERROR: Block size is too large for the key and symbol set size. "
                 "Did you specify the correct key file and encrypted file?")
    # Encrypt message
    encrypted_blocks = encryptMessage(message, (n, e), blockSize)

    # Convert large int values to one string value
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ','.join(encrypted_blocks)

    # Write out encrypted string to output file
    encrypted_content = f"{len(message)}_{blockSize}_{encrypted_content}"
    with open(messageFilename, 'w') as fileObj:
        fileObj.write(encrypted_content)
    return encrypted_content

def readAndDecrypt(messageFilename, keyFilename):
    # Using key from key file, read encrypted message from file
    # then decrypt it. Return decrypted message string
    key_size, n, d = readKeyFile(keyFilename)

    # Read message length and encrypted message from file
    with open(messageFilename, 'r') as fileObj:
        content = fileObj.read()
    message_length, block_size, encrypted_message = content.split('_')
    message_length = int(message_length)
    block_size = int(block_size)

    # Check key size is large enough for block size
    if not (math.log(2 ** key_size, len(SYMBOLS)) >= block_size):
        sys.exit("ERROR: Block size is too large for the key and symbol set size. "
                 "Did you specify the correct key file and encrypted file?")
    # Convert encrypted message into large int values
    encrypted_blocks = []
    for block in encrypted_message.split(','):
        encrypted_blocks.append(int(block))

    # Decrypt large int values
    return decryptMessage(encrypted_blocks, message_length, (n, d), block_size)

# If publicKeyCipher.py is run (instead of imported as module)
# call main() function
if __name__ == '__main__':
    main()