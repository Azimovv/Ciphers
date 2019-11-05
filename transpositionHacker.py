# Transposition Cipher Hacker

import detectEnglish, transpositionDecrypt

def main():
    message = "AaKoosoeDe5 b5sn ma reno ora'lhlrrceey e  enlh na  " \
              "indeit n uhoretrm au ieu v er Ne2 gmanw,forwnlbsya apor " \
              "tE.no euarisfatt  e mealefedhsppmgAnlnoe(c -or)alat r lw o " \
              "eb  nglom,Ain one dtes ilhetcdba. t tg eturmudg,tfl1e1 v  " \
              "nitiaicynhrCsaemie-sp ncgHt nie cetrgmnoa yc r,ieaa  toesa- " \
              "e a0m82e1w shcnth  ekh gaecnpeutaaieetgn iodhso d ro hAe " \
              "snrsfcegrt NCsLc b17m8aEheideikfr aBercaeu thllnrshicwsg " \
              "etriebruaisss  d iorr."

    hacked_message = hackTransposition(message)

    if hacked_message == None:
        print("Failed to hack encryption")

def hackTransposition(message):
    print("Press Ctrl+C to quit (Ctrl+D on macOS or Linux)")

    # Brute force by looping through every possible key
    for key in range(1, len(message)):
        print(f"Trying key: {key}...")
        decrypted_text = transpositionDecrypt.decryptMessage(key, message)

        if detectEnglish.isEnglish(decrypted_text):
            print("\nPossible encryption hack: ")
            print(f"Key: {key}, text: {decrypted_text[:100]}")
            response = input("Enter 'D' if done, anything else to continue: ")
            if response == 'D':
                return decrypted_text
            else:
                continue

    return None


if __name__ == '__main__':
    main()