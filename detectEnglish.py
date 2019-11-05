# Detect English module
# Usage: import detectEnglish
#        detectEnglish.isEnglish(string)
#        returns either True or False

UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'

def loadDictionary():
    filename = 'dictionary.txt'
    english_words = {}
    with open(filename, 'r') as fileObj:
        for word in fileObj.read().split('\n'):
            english_words[word] = None
    return english_words

ENGLISH_WORDS = loadDictionary()

def getEnglishCount(message):
    message = message.upper()
    message = removeNonLetters(message)
    possible_words = message.split()

    if possible_words == []:
        return 0.0 # No words so return 0.0

    matches = 0
    for word in possible_words:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches) / len(possible_words)

def removeNonLetters(message):
    letters = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            letters.append(symbol)
    return ''.join(letters)

def isEnglish(message, word_percent = 20, letter_percent = 85):
    # By default, 20% of words must be in dictionary file,
    # 85% of characters must be letters or spaces (not punctuation or numbers)
    words_match = getEnglishCount(message) * 100 >= word_percent
    num_letters = len(removeNonLetters(message))
    message_letters_percent = float(num_letters) / len(message) * 100
    letters_match = message_letters_percent >= letter_percent
    return words_match and letters_match