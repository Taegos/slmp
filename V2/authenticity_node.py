from utility.crypto_helper import sign, verify, generate_key_pair
from utility.signed_message import SignedMessage
from V2.authenticity_message import AuthenticityMessage
from V2.certificate_authority import certificate_authority
from vanilla.slmp_node import SLMPNode

class AuthenticityNode:

    def __init__(self, context, timeout=5):
        key_pair = generate_key_pair()
        self.__private_key = key_pair.private
        self.__public_key = key_pair.public
        self.__ca_public_key = certificate_authority.get_public_key()
        certificate = certificate_authority.issue_certificate(self.__public_key)
        verify(certificate.identity, self.__ca_public_key, certificate.signature)
        self.__certificate = certificate
        self.__node = SLMPNode(self.__certificate.identity.id, context, timeout)

    def send(self):
        slmp_payload = self.__node.send()
        content = AuthenticityMessage(self.__certificate, slmp_payload)
        signature = sign(content, self.__private_key)
        return SignedMessage(signature, content)

    def receive(self, signed_message):
        content = signed_message.content
        signature = signed_message.signature
        certificate = content.certificate
        identity = certificate.identity
        public_key = certificate.identity.public_key
        verify(content, public_key, signature)
        verify(identity, self.__ca_public_key, certificate.signature)
        self.__node.receive(content.slmp_payload)

    def act(self):
        self.__node.act()

    def as_displayable(self):
        return self.__node.as_displayable()

    def get_id(self):
        return self.__node.get_id()

