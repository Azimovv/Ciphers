# Transposition Cipher Decryption

import math

def main():
    my_message = input("Enter a message to decrypt via transposition: ")
    my_key = int(input("Enter a key for the decryption: "))

    plaintext = decryptMessage(my_key, my_message)

    # Print with a | after incase there are spaces at the end
    print(plaintext + '|')

def decryptMessage(key, message):
    # Simulate the 'columns' and 'rows' of the grid that the plaintext is
    # written on by using a list of strings.

    # Number of 'columns'
    num_columns = int(math.ceil(len(message) / float(key)))
    # Number of 'rows'
    num_rows = key
    # Number of 'shaded boxes'
    num_shaded = (num_columns * num_rows) - len(message)

    # Each string in plaintext represents a column
    plaintext = [''] * num_columns

    # Column and row variables point to next char position in grid
    column = 0
    row = 0

    for symbol in message:
        plaintext[column] += symbol
        column += 1 # Point to next position

        # If no more columns or next pos. is a shaded box,
        # go back to first column on next row
        if (column == num_columns) or (column == num_columns - 1 and
                                       row >= num_rows - num_shaded):
            column = 0
            row += 1

    return ''.join(plaintext)

# If transpositionDecrypt.py is run (instead of imported as module)
# call the main() function
if __name__ == '__main__':
    main()