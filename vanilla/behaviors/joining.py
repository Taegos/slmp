from vanilla.messages.join_request import JoinRequest
from vanilla.messages.message import Message
from vanilla.behaviors.behavior import Behavior


class Joining(Behavior):
    def __init__(self, behavior_data):
        super().__init__("Joining", behavior_data)
        self.__installed_view = None

    def send(self):
        content = JoinRequest(self._data.id, self._data.leader_id)
        return Message("JOIN_REQUEST", content)

    def receive(self, message):
        if message.type == "VIEW_BROADCAST" and \
           message.content.sender_id == self._data.leader_id and \
           message.content.context == self._data.context and \
           self._data.id in message.content.follower_ids:
            self.__installed_view = message.content

    def act(self):
        from vanilla.behaviors.waiting import Waiting
        from vanilla.behaviors.following import Following
        if self.__installed_view is not None:
            return Following(self._data)
        return Waiting(self._data)
