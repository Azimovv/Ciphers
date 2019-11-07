# Vigenere Cipher Dictionary Hacker

import detectEnglish, vigenereCipher

def main():
    ciphertext = "Tzx isnz eccjxkg nfq lol mys bbqq I lxcz."
    hacked_message = hackVigenereDictionary(ciphertext)

    if hacked_message != None:
        print(hacked_message)
    else:
        print("Failed to hack encryption")

def hackVigenereDictionary(ciphertext):
    filename = 'dictionary.txt'
    with open(filename, 'r') as fileObj:
        words = fileObj.readlines()

    for word in words:
        word = word.strip()  # Remove the newline at end
        decrypted_text = vigenereCipher.decrypt_message(word, ciphertext)
        if detectEnglish.isEnglish(decrypted_text, word_percent=40):
            # Check with user to see if decrypted key has been found
            print("\nPossible encryption break: ")
            print(f"Key {str(word)} : {decrypted_text[:100]}")
            response = input("Enter 'D' for done, or ENTER to continue: ")
            if response == 'D' or response == 'd':
                return decrypted_text


if __name__ == '__main__':
    main()