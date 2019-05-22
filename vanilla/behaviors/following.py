from vanilla.messages.notification import Notification
from vanilla.messages.message import Message
from vanilla.behaviors.behavior import Behavior


class Following(Behavior):
    def __init__(self, behavior_data, installed_view):
        super().__init__("Following", behavior_data)
        self.__installed_view = installed_view
        self.__leader_age = 0

    def send(self):
        content = Notification(self._data.leader_id, self._data.leader_id, self.__leader_age)
        return Message("NOTIFICATION", content)

    def receive(self, message):
        if message.type == "VIEW_BROADCAST" and \
           message.content.sender_id == self._data.leader_id:
            self.__leader_age = 0
            self.__installed_view = message.content

    def act(self):
        from vanilla.behaviors.leading import Leading
        self.__leader_age += 1
        if self.__leader_age > self._data.timeout:
            return Leading(self._data)
