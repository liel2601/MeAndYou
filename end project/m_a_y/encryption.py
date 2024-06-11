import binascii
from base64 import b64decode, b64encode

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5


def create_rsa_keys(client_socket):
    """generates an RSA public and private key and send the public one to
    the client_socket that the function receives.
    the function returns both keys"""
    key = RSA.generate(2048)
    pub_key = key.public_key()
    public_key = pub_key.export_key('PEM')
    client_socket.send(len(public_key).to_bytes(4, "big"))
    client_socket.send(public_key)
    print("RSA key has been sent :D")
    return key, pub_key


def rsa_encryption(public_key, data):
    """receives an RSA public key and encrypts data with it"""
    cipher = PKCS1_v1_5.new(public_key)
    return b64encode(cipher.encrypt(data))


def rsa_decryption(private_key, data):
    """receives an RSA private key and decrypts data with it"""
    decryptor = PKCS1_v1_5.new(private_key)
    print(len(data))
    return decryptor.decrypt(b64decode(data), "didn't work".encode())


def do_encrypt(key, iv, data):
    """receives an AES key and iv, and encrypts data with them"""
    obj = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = obj.encrypt(data)
    return ciphertext


def do_decrypt(key, iv, data):
    """receives an AES key and iv, and decrypts data with them"""
    obj2 = AES.new(key, AES.MODE_CFB, iv)
    message = obj2.decrypt(data)
    return message


