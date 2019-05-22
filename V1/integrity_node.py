from utility.crypto_helper import sign, verify, generate_key_pair
from utility.signed_message import SignedMessage
from V1.integrity_message import IntegrityMessage
from vanilla.slmp_node import SLMPNode


class IntegrityNode:

    def __init__(self, context, _id, timeout=5):
        self.__node = SLMPNode(context, _id, timeout)
        key_pair = generate_key_pair()
        self.__public_key = key_pair.public
        self.__private_key = key_pair.private

    def send(self):
        slmp_payload = self.__node.send()
        content = IntegrityMessage(self.__public_key, slmp_payload)
        signature = sign(content, self.__private_key)
        return SignedMessage(signature, content)

    def receive(self, signed_message):
        content = signed_message.content
        signature = signed_message.signature
        public_key = content.public_key
        verify(content, public_key, signature)
        self.__node.receive(content.slmp_payload)

    def act(self):
        self.__node.act()

    def as_displayable(self):
        return self.__node.as_displayable()

    def get_id(self):
        return self.__node.get_id()

