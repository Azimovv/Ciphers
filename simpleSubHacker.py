# Simple Substitution Cipher Hacker

import re, copy, simpleSubCipher, wordPatterns, makeWordPatterns

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')


def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia ' \
              'esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr ' \
              'pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ' \
              'ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu ' \
              'sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia ' \
              'rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao jisr elh. ' \
              '- Facjclxo Ctrram'

    # Determine possible valid ciphertext translations
    print("Attempting to break...")
    letter_mapping = hackSimpleSub(message)

    # Display results to user
    print("Mapping: ")
    print(letter_mapping)
    print("\nOriginal ciphertext: ")
    print(message)
    hacked_message = decryptWithCipherLetterMapping(message, letter_mapping)
    print("\n" + hacked_message)

def getBlankCipherLetterMapping():
    # Returns a dictionary value that is a blank cipherletter mapping
    cipherletter_mapping = {}
    for letter in LETTERS:
        cipherletter_mapping.update({letter: []})
    return cipherletter_mapping

def addLettersToMapping(letterMapping, cipherword, candidate):
    """
    Adds letters in candidate as potential decryption letters for
    cipherletters in the cipherletter mapping
    :param letterMapping: dict value that stores cipherletter mapping
    :param cipherword: string value of cipherword text
    :param candidate: possible English word that cipherword could decrypt to
    """
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])

def intersectMappings(mapA, mapB):
    # Intersect two maps, create blank map and add only potential
    # decryption letters if they exist in BOTH maps
    mapping = getBlankCipherLetterMapping()
    for letter in LETTERS:
        # Empty list means any letter is possible
        # so copy the other map entirely
        if mapA[letter] == []:
            mapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            mapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If letter in mapA[letter] exists in mapB[letter],
            # add that letter to mapping[letter]
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    mapping[letter].append(mappedLetter)

    return mapping

def removeSolvedLetters(letterMapping):
    # Cipherletters in mapping that map to only one letter are
    # solved and can be removed from other letters

    loop_again = True
    while loop_again:
        # Assume another loop won't happen
        loop_again = False

        # solvedLetters will be in a list of uppercase letters that have
        # one and only one possible mapping
        solved_letters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solved_letters.append(letterMapping[cipherletter][0])

        # If a letter is solved then it can't be a potential decryption
        # letter for a different ciphertext letter, so remove it
        for cipherletter in LETTERS:
            for s in solved_letters:
                if len(letterMapping[cipherletter]) != 1 and s in \
                   letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # Letter solved, loop again
                        loop_again = True
    return letterMapping

def hackSimpleSub(message):
    intersectedMap = getBlankCipherLetterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()
    for cipherword in cipherwordList:
        # Get new cipherletter mapping for each ciphertext word
        candidateMap = getBlankCipherLetterMapping()

        word_pattern = makeWordPatterns.getWordPattern(cipherword)
        if word_pattern  not in wordPatterns.allPatterns:
            continue # word not in dictionary, so carry on

        # Add letters of each candidate to mapping
        for candidate in wordPatterns.allPatterns[word_pattern]:
            addLettersToMapping(candidateMap, cipherword, candidate)

        # Intersect the new mapping with existing intersected mapping
        intersectedMap = intersectMappings(intersectedMap, candidateMap)

    # Remove any solved letters from the other lists
    return removeSolvedLetters(intersectedMap)

def decryptWithCipherLetterMapping(ciphertext, letterMapping):
    # Return string of ciphertext decrypted with letter mapping
    # with any ambiguous decrypted letters replaced with  an underscore

    # Create simple sub key from letterMapping
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            # If only one letter add it to key
            key_index = LETTERS.find(letterMapping[cipherletter][0])
            key[key_index] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With key created, decrypt ciphertext
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()