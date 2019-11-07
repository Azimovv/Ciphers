# Vigenere Cipher Hacker

import itertools, re
import vigenereCipher, freqAnalysis, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 16  # Longest key size that will be attempted
NUM_MOST_FREQ_LETTERS = 4  # Letters per subkey attempted
SILENT_MODE = False  # Set to 'True' to run without printing
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def main():
    filename = 'vigenereHackerSampleText.txt'
    with open(filename, 'r') as fileObj:
        ciphertext = fileObj.read()
    hacked_message = hackVigenere(ciphertext)

    if hacked_message != None:
        print(hacked_message)
    else:
        print("Failed to break encryption.")

def findRepeatSequences(message):
    # Parse message finding 3 to 5 letter sequences that are repeated.
    # Return dict with keys of the sequence and values of list of spacings
    # (num of letters between the repeats)

    # Use regular expression to remove non-letters from message
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile list of seqLen-letter sequences found in message
    seq_spacings = {}  # Keys = sequences, values = lists of int spacings
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Find sequence and store it
            seq = message[seqStart:seqStart + seqLen]

            # Look for sequence in rest of message
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # If repeated sequence found
                    if seq not in seq_spacings:
                        seq_spacings[seq] = []  # Initialize empty list

                    # Append spacing distance between repeated sequence and
                    # original sequence
                    seq_spacings[seq].append(i - seqStart)
    return seq_spacings

def getUsefulFactors(num):
    # Returns list of factors less than MAX_KEY_LENGTH + 1 and not 1
    # ex: getUsefulFactors(144) returns [2, 3, 4, 6, 8, 9, 12, 16]

    if num < 2:
        return []  # Num < 2 have no useful factors

    factors = []  # List of factors found

    # Only need to check integers up to MAX_KEY_LENGTH
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            other_factor = int(num / i)
            if other_factor < MAX_KEY_LENGTH + 1 and other_factor != 1:
                factors.append(other_factor)
    return list(set(factors))  # Remove duplicates

def getIndexOne(x):
    return x[1]

def getMostCommonFactors(seq_factors):
    # Get count of how many times a factor occurs in seq_factors
    factor_counts = {}  # Key = factor, value = frequency

    # seq_factors keys are sequences, values are lists factors of spacings
    for seq in seq_factors:
        factor_list = seq_factors[seq]
        for factor in factor_list:
            if factor not in factor_counts:
                factor_counts[factor] = 0
            factor_counts[factor] += 1

    # Put factor and its count into tuple and make list of tuples to sort
    factors_by_count = []
    for factor in factor_counts:
        # Exclude factors > MAX_KEY_LENGTH
        if factor <= MAX_KEY_LENGTH:
            # factors_by_count is list of tuples
            # ex: [(3, 497), (2, 487), ...]
            factors_by_count.append((factor, factor_counts[factor]))

    # Sort list by factor count
    factors_by_count.sort(key=getIndexOne, reverse=True)

    return factors_by_count

def kasiskiExamination(ciphertext):
    # Find sequences of 3-5 letters that occur multiple times
    # ciphertext.repeatedSeqSpacings looks like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ...}
    repeated_spacings = findRepeatSequences(ciphertext)

    seq_factors = {}
    for seq in repeated_spacings:
        seq_factors[seq] = []
        for spacing in repeated_spacings[seq]:
            seq_factors[seq].extend(getUsefulFactors(spacing))

    factors_by_count = getMostCommonFactors(seq_factors)

    # Extract factor counts from factors_by_count into likely_key_lengths
    likely_key_lengths = []
    for twoIntTuple in factors_by_count:
        likely_key_lengths.append(twoIntTuple[0])

    return likely_key_lengths

def getNthSubkeysLetters(nth, keyLength, message):
    # Returns every nth letter for each keyLength set of letters in text
    # ex: getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'

    # Use regular expression to remove non-letters from message
    message = NONLETTERS_PATTERN.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # Determine most likely letters for each letter in key
    ciphertext_up = ciphertext.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists
    # inner lists are freq_scores lists
    all_freq_scores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nth_letters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertext_up)

        # freq_scores is list of tuples, sorted by match score (higher = better match)
        freq_scores = []
        for possibleKey in LETTERS:
            decrypted_text = vigenereCipher.decrypt_message(possibleKey, nth_letters)
            key_freq_tuple = (possibleKey, freqAnalysis.englishFreqMatch(decrypted_text))
            freq_scores.append(key_freq_tuple)
        # Sort by match score
        freq_scores.sort(key=getIndexOne, reverse=True)

        all_freq_scores.append(freq_scores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(all_freq_scores)):
            print(f"Possible letters for letter {i+1} of the key: ", end='')
            for freqScore in all_freq_scores[i]:
                print(f"{freqScore[0]} ", end='')
            print()

    # Try every combination of most likely letters for each position in key
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # Create possible key from letters in all_freq_scores
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += all_freq_scores[i][indexes[i]][0]

        if not SILENT_MODE:
            print(f"Attempting with key: {possibleKey}")

        decrypted_text = vigenereCipher.decrypt_message(possibleKey, ciphertext_up)

        if detectEnglish.isEnglish(decrypted_text):
            # Set hacked ciphertext to original casing
            orig_case = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    orig_case.append(decrypted_text[i].upper())
                else:
                    orig_case.append(decrypted_text[i].lower())
            decrypted_text = ''.join(orig_case)

            # Check with user to see if key is found
            print(f"Possible encryption break with key {possibleKey}: ")
            print(decrypted_text[:200])
            response = input("\nEnter 'D' if done, ENTER to continue: ")
            if response == 'D' or response == 'd':
                return decrypted_text

    # No English-looking decryption found, return None
    return None

def hackVigenere(ciphertext):
    # Do Kasiski examination to find what length of ciphertext's
    # encryption key is
    likely_key_lengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        key_length_str = ''
        for keyLength in likely_key_lengths:
            key_length_str += f"{keyLength} "
        print(f"Kasiski examination results say the most likely key lengths are: "
              f"{key_length_str} \n")
    hacked_message = None
    for keyLength in likely_key_lengths:
        if not SILENT_MODE:
            print(f"Attempting hack with key length {keyLength} "
                  f"({NUM_MOST_FREQ_LETTERS ** keyLength} possible keys)...")
        hacked_message = attemptHackWithKeyLength(ciphertext, keyLength)
        if hacked_message != None:
            break

    # If none of the key lengths found using Kasiski examination worked
    # start brute-forcing through key lengths
    if hacked_message == None:
        if not SILENT_MODE:
            print("Unable to hack message with likely key length(s). Brute-"
                  "forcing key length...")
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # Don't recheck key lengths already tried in Kasiski
            if keyLength not in likely_key_lengths:
                if not SILENT_MODE:
                    print(f"Attempting hack with key length {keyLength} "
                          f"({NUM_MOST_FREQ_LETTERS ** keyLength} possible keys)...")
                hacked_message = attemptHackWithKeyLength(ciphertext, keyLength)
                if hacked_message != None:
                    break
    return hacked_message

# If vigenereHacker.py is run (instead of imported as module)
# call main() function
if __name__ == '__main__':
    main()