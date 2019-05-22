from vanilla.slmp_node import SLMPNode


class Factory:

    def __init__(self, timeout):
        self.__timeout = timeout
        self.__incremental_id = 0

    def create(self, context):
        self.__incremental_id += 1
        return SLMPNode(self.__incremental_id, context, self.__timeout)
