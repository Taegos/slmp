from vanilla.messages.view_broadcast import ViewBroadcast
from vanilla.messages.message import Message
from vanilla.behaviors.behavior import Behavior


class Leading(Behavior):

    """The leading behavior. A node starts here and changes to this
    from waiting and following behavior when their leader times out.

    The purpose of this behavior is to establish membership. It sends
    out a view to every other node. The nodes can request to participate 
    and if this leader recieves the request the node will be accepted 
    and included in the view send out in the next round. Note that
    the context is the same for every member. 
    
    Args:
        state (BehaviorState): The state that is read and written
        to by different behaviors.
    """

    def __init__(self, behavior_data):
        super().__init__("Leading", behavior_data)
        self._data.leader_id = self._data.id
        self.__follower_timers = {}
        self.__follower_ids = []
        self.__last_message_from = {}

    def send(self):
        content = ViewBroadcast(self._data.id, self._data.context, self.__follower_ids)
        return Message("VIEW_BROADCAST", content)

    def receive(self, message):
        if message.type == "VIEW_BROADCAST" and \
           message.content.context == self._data.context and \
           self.__better_leader(message.content.sender_id):
            self._data.leader_id = message.content.sender_id
        else:
            self.__last_message_from[message.content.sender_id] = message

    def act(self):
        """If a better leader was found return joining behavior, else
        continues leading and removes followers that timed out.

        Returns:
            obj: The next behavior, None if the behavior does not change.
        """
        from vanilla.behaviors.joining import Joining
        if self._data.leader_id != self._data.id:
            return Joining(self._data)
        for sender_id in self.__last_message_from.keys():
            message = self.__last_message_from[sender_id]
            content = message.content
            if message.type == "JOIN_REQUEST" and \
               content.sender_id not in self.__follower_ids:
                self.__follower_ids.append(content.sender_id)
                self.__follower_timers[content.sender_id] = 0
            elif message.type == "NOTIFICATION" and \
                 content.sender_id in self.__follower_ids:
                self.__follower_timers[content.sender_id] = content.leader_age
        for follower_id in self.__follower_ids:
            follower_age = self.__follower_timers[follower_id]
            if follower_age > self._data.timeout:
                self.__follower_ids.remove(follower_id)
                del self.__follower_timers[follower_id]
            else:
                follower_age += 1
                self.__follower_timers[follower_id] = follower_age
        self.__last_message_from.clear()

    def __better_leader(self, leader_id):
        return leader_id != self._data.leader_id and leader_id < self._data.leader_id

