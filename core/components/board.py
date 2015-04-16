#!/usr/bin/env python3

from os import path as ospath
from .pieces import Knight, King


class Board:

    def __init__(self):
        self._construct_board()

    def _construct_board(self):
        # TODO save common vals like board size, etc in a common config using:
        # - modules: Simplest way, but requires file creation
        # - create a new class or use one / singleton pattern: Complex
        # - Save to this Class (not instance): Race conditions, Stale on each move?

        readData = self._get_string()
        readRows = readData.split("\n")

        self.state = ()
        self.piecesInBoard = {
            'd': set(),
            'l': set(),
        }
        for i, col in enumerate(readRows):
            col = col.split("|")
            col.pop(0)
            col.pop(len(col)-1)
            colVal = ()
            for j, cell in enumerate(col):
                piece = self._get_piece_from_string(cell)
                if piece is not None:
                    self.piecesInBoard[piece.team].add(piece.__class__)
                    piece.row = i
                    piece.column = j
                if isinstance(piece, King):
                    setattr(self, cell, piece)
                colVal += (piece, )
            self.state += (colVal, )

    def _get_string(self):
        root = (ospath.dirname(
            ospath.dirname(
                ospath.dirname(
                    ospath.abspath(__file__)))))
        with open('{0}/usr/input.txt'.format(root), "r") as f:
            readData = f.read()
        return readData

    def _get_piece_from_string(self, string):
        if string == '  ':
            return None
        else:
            pieceTypes = {
                'k': King,
                'n': Knight
            }
            team = string[1]
            return pieceTypes[string[0]](team)

    def _get_state(self):
        return self.state

    def _get_peices_in_board(self):
        return self.piecesInBoard

    def print_broard(self):
        string = ''
        for row in self.state:
            string += "|"
            for cell in row:
                if cell is None:
                    string += '  '
                else:
                    # TODO do below by dict
                    string += str(cell)
                string += "|"
            string += "\n"
        print(string)

    def is_white_in_check(self):
        """Thin wrapper for is_checked"""

        return self.is_checked('white')

    def is_black_in_check(self):
        """Thin wrapper for is_checked"""

        return self.is_checked('black')

    def is_checked(self, team):
        """Checks if the king for the given team is checked"""

        k = self._get_king_for_team(team)
        return True if self._hunters_watching(k) else False

    # def _get_possible_moves(self, piece):
    #     if isinstance(piece, Knight):
    #         rows =

    # TODO convert below two functions into one for better optimization

    def _hunters_watching(self, piece):
        possibleKillZones = self._get_killzones(piece)

        hunters = ()
        # TODO trivial solution. Make better
        for kz in possibleKillZones:
            square = self.state[kz[0]][kz[1]]
            if square is not None and square.team != piece.team:
                hunters += (square, )

        return hunters or False

    def _get_killzones(self, piece):
        killzones = set()
        for p in self.piecesInBoard[get_opposing_team_char(piece)]:
            killzones.update((piece.row+move[0], piece.column+move[1])
                    for move in p.baseMoves
                    if piece.row+move[0] > 0 and piece.column+move[1] > 0)
        return killzones

    # def _hunters_watching(self, piece):
    #     hunters = ()
    #     for ememyClass in self.piecesInBoard[get_opposing_team_char(piece)]:
    #         for move in ememyClass.baseMoves:
    #             print("##")
    #             print(move)
    #             print("##")
    #             r = piece.row+move[0]
    #             c = piece.column+move[1]
    #             square = self.state[r][c]
    #             if square is not None and square.team != piece.team:
    #                 print(square, r, c)
    #                 hunters += (square, )
    #     return hunters or False

    def allowed_moves(self, peice):
        """Checks the given moves list and returns the possible moves for the
        piece"""

        allowedMoves = ()
        for move in peice.abstract_moves():
            attempt = self.state[move[0]][move[1]]
            if (attempt is None or
                    attempt.team != peice.team):
                allowedMoves += (move, )
        return allowedMoves

    def is_white_in_checkmate(self):
        return self.is_checkmate('white')

    def is_black_in_checkmate(self):
        return self.is_checkmate('black')

    def is_checkmate(self, team):

        k = self._get_king_for_team(team)
        hunters = self._hunters_watching(k)
        if not hunters:
            return False

        # if there is only one hunter attempt to kill it.
        if len(hunters) == 1:
            if self._hunters_watching(hunters[0]):
                return False

        # So that failed. Attempt to make the king escape
        kOldRow = k.row
        kOldColumn = k.column
        for move in self.allowed_moves(k):
            k.row = move[0]
            k.column = move[1]
            
            # print("king is at {0}".format((k.row, k.column)))

            if not self._hunters_watching(k):
                return False

            # print("Hunters: {0}".format([(i, (i.row, i.column)) for i in self._hunters_watching(k)]))
            k.row = kOldRow
            k.column = kOldColumn
        else:
            return True

    def _get_king_for_team(self, team):
        try:
            if team in ('white', 'light', 'l'):
                return self.kl
            elif team in ('black', 'dark', 'd'):
                return self.kd
        except AttributeError:
            raise Exception("The king for team '{0}' does not exist. "
                    "The game is already lost!".format(team))

def get_opposing_team_char(piece):
    return 'd' if piece.team == 'l' else 'l'
