# Transposition Cipher Encrypt/Decrypt File

import time, os, sys, transpositionEncrypt, transpositionDecrypt

def main():
    input_filename = 'frankenstein.txt'
    output_filename = 'frankenstein.encrypted.txt'
    key = 10
    mode = 'encrypt' # Can be set to either 'encrypt' or 'decrypt'

    # If input file doesn't exist, terminate early
    if not os.path.exists(input_filename):
        print(f"File '{input_filename}' does not exist. Quitting...")
        sys.exit()

    # If output file already exists, give user chance to exit
    if os.path.exists(output_filename):
        response = input("File already exists, would you like to continue? (y/n) ")
        if response != 'y':
            sys.exit()

    # Read input file
    with open(input_filename, 'r') as fileObj:
        content = fileObj.read()

    print(f"{mode.title()}ing...")

    # Measure how long encryption/decryption takes
    startTime = time.time()
    if mode == 'encrypt':
        translated = transpositionEncrypt.encryptMessage(key, content)
    elif mode == 'decrypt':
        translated = transpositionDecrypt.decryptMessage(key, content)
    totalTime = round(time.time() - startTime, 2)
    print(f"{mode.title()}ion time: {totalTime} seconds")

    # Write out translated message to output file
    with open(output_filename, 'w') as fileObj:
        fileObj.write(translated)

    print(f"Done {mode}ing {input_filename} ({len(content)}).")
    print(f"{mode.title()}ed file is {output_filename}.")

# If transpositionCipherFile.py is run (instead of imported as module)
# call 'main()' function
if __name__ == '__main__':
    main()