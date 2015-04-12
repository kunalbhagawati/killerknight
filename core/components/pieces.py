"""Module to hold the pieces"""


class Piece:

    def __init__(self, team):
        if team not in ('d', 'l'):
            raise Exception("Unknown team {0} passed.".format(team))
        self.team = team

    def __str__(self, letter):
        return letter+self.team


class King(Piece):

    def __str__(self):
        return super().__str__('k')


class Knight(Piece):

    def __str__(self):
        return super().__str__('n')
