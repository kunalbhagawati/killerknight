"""Module to hold the Moveset class"""


class Moveset:

    def __init__(self, rowMax, rowMin, columnMax, columnMin, **kwargs):
        pass


class FixedMoveset:

    def __init__(self, rowDiff, colDiff, **kwargs):

        super().__init__(rowDiff, rowDiff, colDiff, colDiff)

    def _get_possible_moves(self):
        
