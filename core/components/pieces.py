"""Module to hold the pieces"""

from .moveset import FixedMoveset


class Piece:

    def __init__(self, team):
        if team not in ('d', 'l'):
            raise Exception("Unknown team {0} passed.".format(team))
        self.team = team

    def __str__(self, letter):
        return letter+self.team


class FixedMovePiece(Piece):

    def __init__(self, team):
        self.moveset = FixedMoveset(self)
        super().__init__(team)

    def abstract_moves(self):
        """Gets the cells that can be traversed by this peice.
        This includes the cells that are occupied by other peices."""

        return self.moveset.abstract_moves()

    def move(self, newLocTuple):
        return self.moveset.move(newLocTuple)


class King(FixedMovePiece):

    baseMoves = (
            (-1, +0),
            (-1, +1),
            (-1, -1),
            (+0, +0),
            (+0, +1),
            (+0, -1),
            (+1, +0),
            (+1, +1),
            (+1, -1),
            )

    def __str__(self):
        return super().__str__('k')


class Knight(FixedMovePiece):

    baseMoves = (
            (+2, +1),
            (+2, -1),
            (-2, +1),
            (-2, -1),
            (+1, +2),
            (+1, -2),
            (-1, +2),
            (-1, -2),
            )

    def __str__(self):
        return super().__str__('n')
