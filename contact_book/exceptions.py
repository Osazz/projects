class NoAction(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class MissingVariable(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class WrongVariable(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class TooLongVariable(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
