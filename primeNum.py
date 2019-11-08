# Prime Number Sieve

import math, random

def isPrimeTrialDiv(num):
    # Returns True if num is a prime number, otherwise False
    # Use trial division algorithm for testing primality

    # All num less than 2 are not prime
    if num < 2:
        return False

    # Check num divisibility of numbers up to square root of num
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def primeSieve(sieveSize):
    # Return list of prime numbers calculated by the Sieve of Eratosthenes
    sieve = [True] * sieveSize
    sieve[0] = False  # 0 and 1 are not prime
    sieve[1] = False

    # Create sieve
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # Compile list of primes
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes

def rabinMiller(num):
    # Return True if num is prime
    if num % 2 == 0 or num < 2:
        return False  # Rabin-Miller doesn't work on even ints
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        # Keep halving s until it's odd
        # Use t to keep count of amount times s is halved
        s = s // 2
        t += 1
    for trials in range(5):  # Try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # Test doesn't apply if v is 1
            i = 0
            while v != (num-1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % num
    return True

LOW_PRIMES = primeSieve(100)

def isPrime(num):
    # Return True if num is prime
    # Quicker check before calling rabinMiller()
    if num < 2:
        return False

    # Check if low primes can divide num
    for prime in LOW_PRIMES:
        if num == prime:
            return True
        if num % prime == 0:
            return False

    # Call rabinMiller() if previous method has failed
    return rabinMiller(num)

def generateLargePrime(keysize=1024):
    # Return random prime with bit size of 'keysize'
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize)
        if isPrime(num):
            return num