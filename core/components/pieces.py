"""Module to hold the pieces"""


class Piece:
    
    def __init__(self, team):
        if team not in ('d', 'l'):
            raise Exception("Unknown team {0} passed.".format(team))
        self.team = team


class King(Piece):
    pass


class Knight(Piece):
    pass
