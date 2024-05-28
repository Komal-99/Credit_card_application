import random
import math
from MajorCode import extract_feilds
# A set will be the collection of prime numbers,
# where we can select random primes p and q
prime = set()

public_key = None
private_key = None
n = None
from flask import jsonify

# We will run the function only once to fill the set of
# prime numbers
def primefiller():
    # Method used to fill the primes set is Sieve of
    # Eratosthenes (a method to collect prime numbers)
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False

    # Filling the prime numbers
    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)


# Picking a random prime number and erasing that prime
# number from list because p!=q
def pickrandomprime():
    global prime
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)

    ret = next(it)
    prime.remove(ret)
    return ret


def setkeys():
    global public_key, private_key, n
    prime1 = pickrandomprime()  # First prime number
    prime2 = pickrandomprime()  # Second prime number

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    # d = (k*Φ(n) + 1) / e for some integer k
    public_key = e

    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    private_key = d


# To encrypt the given number
def encrypt(message):
    global public_key, n
    e = public_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text


# To decrypt the given number
def decrypt(encrypted_text):
    global private_key, n
    d = private_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted


# First converting each character to its ASCII value and
# then encoding it then decoding the number to get the
# ASCII and converting it to character
def encoder(message):
    encoded = []
    # Calling the encrypting function in encoding function
    for letter in message:
        encoded.append(encrypt(ord(letter)))
    return encoded


def decoder(encoded):
    s = ''
    # Calling the decrypting function decoding function
    for num in encoded:
        s += chr(decrypt(num))
    return s


def enc(image_path):
    primefiller()
    setkeys()
    account_numbers,expiry_dates,card_types,card_holder_names=extract_feilds(image_path)
    acc_no= account_numbers
    date=expiry_dates
    card=card_types
    name=card_holder_names
    # print(message)
    
    codedvalue_1= encoder(acc_no)
    codedvalue_2=encoder(date)
    codedvalue_3=encoder(card)
    codedvalue_4=encoder(name)
    encoded_acc_no_str = ''.join(str(p) for p in codedvalue_1)
    encoded_date_str = ''.join(str(p) for p in codedvalue_2)
    encoded_card_str = ''.join(str(p) for p in codedvalue_3)
    encoded_name_str = ''.join(str(p) for p in codedvalue_4)
    
    
    print("Initial message:",acc_no,"encrypted",''.join(str(p) for p in codedvalue_1))
    print("Initial message:",date,"encrypted",''.join(str(p) for p in codedvalue_2))
    print("Initial message:",card,"encrypted",''.join(str(p) for p in codedvalue_3))
    print("Initial message:",name,"encrypted",''.join(str(p) for p in codedvalue_4))
   
    data = {
        "account_numbers": acc_no,
        "expiry_dates": date,
        "card_types": card,
        "card_holder_names": name,
        "encoded_account_numbers": encoded_acc_no_str,
        "encoded_expiry_dates": encoded_date_str,
        "encoded_card_types": encoded_card_str,
        "encoded_card_holder_names": encoded_name_str
    }
    return acc_no,date,card,name,encoded_acc_no_str,encoded_date_str,encoded_card_str,encoded_name_str
    


