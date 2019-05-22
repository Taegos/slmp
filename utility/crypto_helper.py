from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from utility.key_pair import KeyPair
import jsonpickle


def generate_key_pair(key_length = 1024):
    key = RSA.generate(key_length)
    public_key = key.publickey().exportKey()
    private_key = key.export_key()
    return KeyPair(private_key, public_key)


def verify(content, public_key, signature):
    json = jsonpickle.encode(content)
    cipher = SHA256.new(json.encode())
    try:
        pkcs1_15.new(RSA.import_key(public_key)).verify(cipher, signature)
    except ValueError as e:
        raise e


def sign(content, private_key):
    json = jsonpickle.encode(content)
    cipher = SHA256.new(json.encode())
    return pkcs1_15.new(RSA.import_key(private_key)).sign(cipher)             