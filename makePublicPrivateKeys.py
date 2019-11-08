# Public Key Generator

import random, sys, os, primeNum, cryptomath

def main():
    # Create public/private keypair with 1024-bit keys
    print("Making key files...")
    makeKeyFiles("sunny_p", 1024)
    print("Key files made.")

def generateKey(keySize):
    # Create public/private keys keySize bits in size
    p = 0
    q = 0
    # Create two primes, p and q. Calculate n = p * q
    print("Generating p prime...")
    while p == q:
        p = primeNum.generateLargePrime(keySize)
        q = primeNum.generateLargePrime(keySize)
    n = p * q

    # Create number e that is relatively prime to (p-1)*(q-1)
    print("Generating e that is relatively prime to (p-1) * (q-1)...")
    while True:
        # Keep trying rand numbers for e until one is valid
        e = random.randrange(2 ** (keySize - 1), 2 ** keySize)
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Calculate d, mod inverse of e
    print("Calculating d that is the mod inverse of e...")
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    print(f"Public key: {publicKey}")
    print(f"Private key: {privateKey}")

    return  publicKey, privateKey

def makeKeyFiles(name, keySize):
    # Create two files "x_pubkey.txt" and "x_privkey.txt" where x is 'name'
    # with n,e and d,e integers written in them delimited by a comma

    # Safety check to prevent overwriting our old key files
    if os.path.exists(f"{name}_pubkey.txt") or os.path.exists(f"{name}_privkey.txt"):
        sys.exit(f"WARNING: The file {name}_pubkey.txt or {name}_privkey.txt "
                 f"already exists, use a different name or delete them and rerun.")

    publicKey, privateKey = generateKey(keySize)

    print(f"\nThe public key is a {len(str(publicKey[0]))} and a "
          f"{len(str(publicKey[1]))} digit number")
    print(f"Writing public key to file {name}_pubkey.txt...")
    with open(f"{name}_pubkey.txt", 'w') as fileObj:
        fileObj.write(f"{keySize},{publicKey[0]},{publicKey[1]}")

    print(f"\nThe private key is a {len(str(privateKey[0]))} and a "
          f"{len(str(privateKey[1]))} digit number")
    print(f"Writing private key to file {name}_privkey.txt...")
    with open(f"{name}_privkey.txt", 'w') as fileObj:
        fileObj.write(f"{keySize},{privateKey[0]},{privateKey[1]}")

# If makePublicPrivateKeys.py is run (instead of imported as a module)
# call the main() function
if __name__ == "__main__":
    main()