class Behavior:
    def __init__(self, display_name, behavior_data):
        self.__display_name = display_name
        self._data = behavior_data

    def as_displayable(self):
        return {
            "id": self._data.id,
            "behavior": self.__display_name,
            "context": self._data.context,
            "leader_id": self._data.leader_id
        }

    def get_id(self):
        return self._data.id

