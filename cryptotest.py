import os
import base64
from collections import Counter
from hashlib import md5
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

def keygen(p): #key generation algorithm

    password = p.encode('utf-8')
    salt = b'Salting is not necessary for this particular use case. You just need a strong password'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, #32-byte key = 256 bits. Not very long if you ask me but 256 is the largest AES can accept. :(((((((
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt(plaintext, p):
    key = keygen(p)
    # Generate a random 96-bit IV.
    iv = os.urandom(12)
    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    return (iv+encryptor.tag+ciphertext)

def decrypt( wholetext, p):
    key = keygen(p)
    iv, tag,ciphertext = wholetext[0:12], wholetext[12:28], wholetext[28:]
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    try:
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
    except:
        print("Could not decrypt. Either key is wrong or file is not valid. Now exiting.")
        exit(1)

def decrypt_line(encoded_line, key):
    try:
        line = base64.b64decode(encoded_line, validate=True)
    except:
        print("Failed to decode base64")
        return None
    checksum, msg = line[0:16], line[16:]
    if md5(msg).digest() != checksum:
        print("Bad checksum, expected:" + md5(msg).hexdigest() + " Got:" + checksum.hex())
        return None
    iv, tag, ciphertext = msg[0:12], msg[12:28], msg[28:]
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    try:
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
    except:
        print("!!!!!!!!!!!!!!!!!!!!!Key most likely incorrect!!!!!!!!!!!!!!!!!!")
        return None
    
def loadfile(lines, p): #this logic is not right yet. Fix it. 
    lines = [x.strip() for x in lines] 
    contents = set()
    results = []
    key = keygen(p)
    for line in lines:
        repeated = line.split(':')
        for rl in repeated:
            result = decrypt_line(rl, key)
            if not (result is None):
                if result not in contents:
                    contents.add(result)
                    results.append(result)
            else:
                pass # An error occurred. 
    return results

def encrypt_line(plaintext_line, p):
    encrypted = encrypt(plaintext_line, p)
    checksum = md5(encrypted).digest()
    return base64.b64encode(checksum+encrypted).decode('utf-8')

def encrypt_lines(lines, p):
    encryptedLines = []
    for line in lines:
        encryptedLines.append(encrypt_line(line, p))
    return encryptedLines

# stuff to run always here such as class/def
def main():
    password = input("Enter your password: ")
    plaintext = input("Enter your plaintext: ")
    wholetext = encrypt(
        plaintext,
        password
    )

    print(decrypt(
        wholetext,
        password
    ))

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
