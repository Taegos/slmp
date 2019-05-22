from utility.crypto_helper import generate_key_pair, sign, verify
from utility.signed_message import SignedMessage
from V2.certificate_authority import certificate_authority
from V3.view_broadcast import ViewsBroadcast
from vanilla.messages.join_request import JoinRequest
from vanilla.messages.notification import Notification


class SLMPServer:

    def __init__(self, _id):
        key_pair = generate_key_pair()
        self.__private_key = key_pair.private
        self.__public_key = key_pair.public
        self.__ca_public_key = certificate_authority.get_public_key()
        self.__views = {}
        self.__follower_timer = {}

        self.__id = _id

    def broadcast(self):
        signature = sign(self.__views, self.__private_key)
        content = ViewsBroadcast(self.__id, self.__views)
        message = SignedMessage(signature, content)
        return message

    def receive(self, signed_message):
        self.__verify_message(signed_message)
        slmp_payload = signed_message.content.slmp_payload
        if isinstance(slmp_payload, JoinRequest):
            pass
        elif isinstance(slmp_payload, Notification):
            pass
        elif isinstance(slmp_payload, ViewsBroadcast):
            pass

    def __handle_join_request(self, join_request):
        pass

    def __handle_views_broadcast(self, views_broadcast):
        pass

    def __handle_notification(self, notification):
        pass

    #def join(self, join_request):
    #    self.__verify_message(signed_message)
    #    join_request = signed_message.content.slmp_payload
    #    context = join_request.context
    #    if context not in self.__views:
    #        self.__views[join_request.context] = [join_request.sender_id]
    #    else:
    #        self.__views[context].append(join_request.sender_id)

    #def notify(self, notification):
    #    self.__verify_message(signed_message)
    #    notification = signed_message.content.slmp_payload

    def __verify_message(self, signed_message):
        content = signed_message.content
        certificate = content.certificate
        identity = certificate.identity
        sender_public_key = certificate.identity.public_key
        verify(content, sender_public_key, signed_message.signature)
        verify(identity, self.__ca_public_key, certificate.signature)