from utility.crypto_helper import generate_key_pair, sign, verify
from utility.signed_message import SignedMessage
from V2.certificate_authority import certificate_authority
from V2.authenticity_message import AuthenticityMessage
from V3.join_request import JoinRequest


class SLMPClient:

    def __init__(self, _id, context):
        key_pair = generate_key_pair()
        self.__private_key = key_pair.private
        self.__public_key = key_pair.public
        certificate = certificate_authority.issue_certificate(self.__public_key)
        self.__certificate = certificate
        self.__ca_public_key = certificate_authority.get_public_key()
        verify(certificate.identity, self.__ca_public_key, certificate.signature)
        self.__id = _id
        self.__context = context
        self.__installed_view = None

    def send(self):
        slmp_payload = JoinRequest(self.__context, self.__id)
        content = AuthenticityMessage(self.__certificate, slmp_payload)
        signature = sign(content, self.__private_key)
        return SignedMessage(signature, content)

    def receive(self, signed_message):
        view_broadcast = signed_message.content
        verify(view_broadcast, self.__ca_public_key, signed_message.signature)
        self.__installed_view = view_broadcast

