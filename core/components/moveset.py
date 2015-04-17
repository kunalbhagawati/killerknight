"""Module to hold the Moveset class"""


class Moveset:

    def __init__(self, **kwargs):
        pass


class FixedMoveset:

    def __init__(self, callerInst, **kwargs):
        self.callerInst = callerInst

    def abstract_moves(self):
        """Gets all possible moves for the peice.
        This includes those squares that overlaps with another peice
        and also those that fall outside the board"""

        moves = set()
        for r in self.callerInst.baseMoves:
            newRow = self.callerInst.row+r[0]
            newCol = self.callerInst.column+r[1]
            if newRow in range(0, 8) and newCol in range(0, 8):
                moves.add((newRow, newCol))
        return moves

    def move(self, newLocTuple):
        self.callerInst.row = newLocTuple[0]
        self.callerInst.column = newLocTuple[1]
        return True
