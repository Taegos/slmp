from vanilla.behaviors.behavior import Behavior

class Waiting(Behavior):
    def __init__(self, behavior_data):
        """The waiting behavior. A node changes to this behavior from
        joining when it does not immediatelly get accepted by the 
        leader in to the view. 

        The purpose of this behavior is to wait for the leader to 
        accept this node. If the node does not get accepted it 
        changes to leader behavior with an emtpy view.
        
        Args:
            state (BehaviorState): The state that is read and written
            to by different behaviors.
        """
        super().__init__("Waiting", behavior_data)
        self.__leader_wait_time = 0
        self.__installed_view = None

    def send(self):

        """A node in the waiting behavior does not send a message.
        """
        pass

    def receive(self, message):
        if message.type == "VIEW_BROADCAST" and \
           message.content.sender_id == self._data.leader_id and \
           message.content.context == self._data.context and \
           self._data.id in message.content.follower_ids:
            self.__installed_view = message.content
     
    def act(self):
        """Determines the next behavior.

        Returns:
            obj: The next behavior.
        """
        from vanilla.behaviors.following import Following
        from vanilla.behaviors.leading import Leading

        if self.__installed_view is not None:
            return Following(self._data, self.__installed_view)
        self.__leader_wait_time += 1
        if self.__leader_wait_time > self._data.timeout:
            return Leading(self._data)
