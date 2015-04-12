"""Module to hold the Moveset class"""


class Moveset:

    def __init__(self, **kwargs):
        pass


class FixedMoveset:

    def __init__(self, callerInst, **kwargs):
        self.callerInst = callerInst

    def _get_possible_moves(self):
        pass
