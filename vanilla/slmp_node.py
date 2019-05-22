from vanilla.behaviors.leading import Leading
from vanilla.behaviors.behavior_data import BehaviorData


class SLMPNode:

    def __init__(self, _id, context, timeout=4):
        self.__behavior = Leading(BehaviorData(_id, context, timeout, _id))

    def send(self):
        return self.__behavior.send()

    def receive(self, message):
        self.__behavior.receive(message)

    def act(self):
        next_behavior = self.__behavior.act()
        if next_behavior is not None:
            self.__behavior = next_behavior

    def as_displayable(self):
        return self.__behavior .as_displayable()

    def get_id(self):
        return self.__behavior.get_id()

