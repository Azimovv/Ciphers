# Frequency Finder

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message
    letter_count = {}
    for letter in LETTERS:
        letter_count.update({letter: 0})

    for letter in message.upper():
        if letter in LETTERS:
            letter_count[letter] += 1

    return letter_count

def getIndexZero(items):
    return items[0]

def getFrequencyOrder(message):
    # Returns string of alphabet letters arranged in order of
    # most frequently occurring in message parameter

    # Get dictionary of each letter and its frequency
    letter_to_freq = getLetterCount(message)

    # Make dictionary of each frequency count to letter
    freq_to_letter = []
    for letter in LETTERS:
        if letter_to_freq[letter] not in freq_to_letter:
            freq_to_letter[letter_to_freq[letter]] = [letter]
        else:
            freq_to_letter[letter_to_freq[letter]].append(letter)

    # Put each list of letters in reverse "ETAOIN" order, convert to string
    for freq in freq_to_letter:
        freq_to_letter[freq].sort(key=ETAOIN.find, reverse=True)
        freq_to_letter[freq] = ''.join(freq_to_letter[freq])

    # Convert freq_to_letter to a list of tuple pairs, then sort
    freq_pairs = list(freq_to_letter.items())
    freq_pairs.sort(key=getIndexZero, reverse=True)

    # Extract all letters for final string
    freq_order = []
    for freq_pair in freq_pairs:
        freq_order.append(freq_pair[1])

    return ''.join(freq_order)

def englishFreqMatch(message):
    # Return number of matches the string in message parameter has
    # when its letter frequency is compared to English letter frequency
    # A 'match' is how many of its six most frequent and six least
    # frequent letters are among the same frequent letters for English
    freq_order = getFrequencyOrder(message)

    match_score = 0
    # How many matches for the six most common letters
    for common in ETAOIN[:6]:
        if common in freq_order[:6]:
            match_score += 1
    # How many matches for the six least common letters
    for uncommon in ETAOIN[-6:]:
        if uncommon in freq_order[-6:]:
            match_score += 1

    return match_score