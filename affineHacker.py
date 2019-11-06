# Affine Cipher Hacker

import affineCipher, detectEnglish, cryptomath

SILENT_MODE = False

def main():
    message = '5QG9ol3La6QI93!xQxaia6faQL9QdaQG1!!axQARLa!!AuaRLQADQALQG93!x' \
              'QxaGaAfaQ1QX3o1RQARL9Qda!AafARuQLX1LQALQI1iQX3o1RN"Q-5!1RQP3' \
              '6ARu'

    hacked_message = hackAffine(message)

    if hacked_message != None:
        # The plaintext is displayed on the screen
        print(hacked_message)
    else:
        print("Failed to hack encryption")

def hackAffine(message):
    print("Attempting break...")
    print("Press Ctrl+C (Ctrl+D for macOS and Linux) to quit.")

    # Brute-Force by looping every possible key
    for key in range(len(affineCipher.SYMBOLS) ** 2):
        keyA = affineCipher.getKeyParts(key)[0]
        if cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) != 1:
            continue
        decrypted_text = affineCipher.decryptMessage(key, message)
        if not SILENT_MODE:
            print(f"Tried Key {key}... {decrypted_text[:40]}")

        if detectEnglish.isEnglish(decrypted_text):
            # Check with user if key has been found
            print("\nPossible encryption hack: ")
            print(f"Key: {key}")
            print(f"Decrypted Message: {decrypted_text[:200]}")
            response = input("\nEnter 'D'  for done, or press Enter to continue: ")
            if response == 'D':
                return decrypted_text
    return None

# If affineHacker.py is run (instead of imported as module), call
# the main() function
if __name__ == '__main__':
    main()