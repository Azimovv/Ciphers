# Reverse a message

message = input("Enter a message to reverse: ")
flipped = ''

for i in range(len(message)-1, -1, -1):
    flipped += message[i]

print(flipped)