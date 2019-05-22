class Debugger:
    __enabled = False
    @classmethod
    def set_enabled(cls, enabled):
        cls.__enabled = enabled

    @classmethod
    def log(cls, message):
        if cls.__enabled:
            print(message)    