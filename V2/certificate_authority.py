from utility.crypto_helper import generate_key_pair, sign
from V2.certificate import Certificate
from V2.identity import Identity

class CertificateAuthority:

    def __init__(self):
        key_pair = generate_key_pair()
        self.__private_key = key_pair.private
        self.__public_key = key_pair.public
        self.__incremental_id = 0

    def get_public_key(self):
        return self.__public_key

    def issue_certificate(self, public_key):
        self.__incremental_id += 1
        identity = Identity(self.__incremental_id, public_key)
        signature = sign(identity, self.__private_key)
        certificate = Certificate(signature, identity)
        return certificate


certificate_authority = CertificateAuthority()