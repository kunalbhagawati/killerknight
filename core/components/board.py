#!/usr/bin/env python3

from os import path as ospath
from .pieces import Knight, King, Piece
from core.config import Config

class Board:

    def __init__(self):
        self._construct_board()

    def _construct_board(self):
        """Construct the board from the input."""

        # TODO save common vals like board size, etc in a common config using:
        # - modules: Simplest way, but requires file creation
        # - create a new class or use one / singleton pattern: Complex
        # - Save to this Class (not instance): Race conditions, Stale on
        # each move?

        readData = self._get_string()
        readRows = readData.split("\n")

        self.state = ()
        self.pieceTypesInBoard = {
            'd': set(),
            'l': set(),
        }
        self.piecesInBoard = {
            'd': (),
            'l': (),
        }

        for i, col in enumerate(readRows):
            col = col.split("|")
            col.pop(0)
            col.pop(len(col)-1)
            colVal = ()
            for j, cell in enumerate(col):
                piece = self._get_piece_from_string(cell)
                if piece is not None:
                    self.pieceTypesInBoard[piece.team].add(piece.__class__)
                    self.piecesInBoard[piece.team] += (piece, )
                    piece.row = i
                    piece.column = j
                if isinstance(piece, King):
                    setattr(self, cell, piece)
                colVal += (piece, )
            self.state += (colVal, )

    def _get_string(self):
        """Gets the string representing the board from the input."""

        root = (ospath.dirname(
            ospath.dirname(
                ospath.dirname(
                    ospath.abspath(__file__)))))
        with open('{0}/usr/input.txt'.format(root), "r") as f:
            readData = f.read()
        return readData

    def _get_piece_from_string(self, string):
        """Get the piece instance from the string passed."""

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
        """Gets the state variable."""

        return self.state

    def _get_peiceTypes_in_board(self, team=None):
        """Gets the classes of the peice types in the board."""

        return (self.pieceTypesInBoard if team is None
                else self.pieceTypesInBoard[team])

    def _get_peices_in_board(self, team=None):
        """Gets the instances of the peices in the board."""

        return (self.piecesInBoard if team is None
                else self.piecesInBoard[team])

    def print_broard(self):
        """Prints the state of the board"""

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

        return True if self.is_checked('white') else False

    def is_black_in_check(self):
        """Thin wrapper for is_checked"""

        return True if self.is_checked('black') else False

    def is_checked(self, team):
        """Checks if the king for the given team is checked"""

        return self._hunters_watching(self._get_king_for_team(team))

    def _hunters_watching(self, piece):
        """Checks the enemy pieces looking at the given piece."""

        hunters = ()
        for ememyClass in (self
                ._get_peiceTypes_in_board(get_opposing_team_char(piece))):
            for move in ememyClass.baseMoves:
                r = piece.row+move[0]
                c = piece.column+move[1]
                dbprint(r, c)
                square = self.state[r][c]
                if (square is not None
                        and square.team != piece.team
                        and isinstance(square, ememyClass)):
                    dbprint("Hunter {0} watching at {1}".format(str(square), (square.row, square.column)))
                    hunters += (square, )
        return hunters or False

    def allowed_moves(self, peice, noKing=False):
        """Checks the given moves list and returns the possible moves for the
        piece."""

        allowedMoves = ()
        for move in peice.abstract_moves():
            attempt = self.state[move[0]][move[1]]
            cond = attempt is None or attempt.team != peice.team
            if noKing:
                cond = cond and not isinstance(attempt, King)
            if cond:
                allowedMoves += (move, )
        return allowedMoves

    def is_white_in_checkmate(self):
        return self.is_checkmate('white')

    def is_black_in_checkmate(self):
        return self.is_checkmate('black')

    def is_checkmate(self, team):
        """Check if the king for the passed team is in checkmate"""

        k = self._get_king_for_team(team)
        hunters = self._hunters_watching(k)
        # dbprint(["Hunter {0} at {1}".format(str(i), (i.row, i.column)) for i in hunters])
        if not hunters:
            return False

        # if there is only one hunter attempt to kill it.
        if len(hunters) == 1:
            if self._hunters_watching(hunters[0]):
                # dbprint(["Hunters watching hunter {0} at {1}".format((str(i)), (i.row, i.column)) for i in self._hunters_watching(hunters[0])])
                return False

        # So that failed. Attempt to make the king escape
        dbprint("Attempt to escape")
        kOldRow = k.row
        kOldColumn = k.column
        for m in self.allowed_moves(k):
            dbprint("King ({0}) moves to {1}".format(k.team, m))
            k.move(m)
            if not self._hunters_watching(k):
                dbprint(["Hunter {0} at {1}".format(str(i), (i.row, i.column)) for i in hunters])
                return False
            k.move((kOldRow, kOldColumn))
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

    def can_black_checkmate_in_one_move(self):
        """Wrapper function for self.is_checkmate_in_one_move()"""

        return self.is_checkmate_in_one_move('l')

    def is_checkmate_in_one_move(self, team):
        """Checks if the team could be checkmated in one move"""

        # for each peice, make a move. Then check if the king is in checkmate
        if team in ('white', 'light', 'l'):
            team = 'l'
        elif team in ('black', 'dark', 'd'):
            team = 'd'

        for piece in self._get_peices_in_board(get_opposing_team_char(team)):
            pieceOldRow = piece.row
            pieceOldColumn = piece.column
            for m in self.allowed_moves(piece, noKing=True):
                oldPiece = self.state[m[0]][m[1]]
                # dbprint("Piece {0} at {1} moves to {2}".format(str(piece), (piece.row, piece.column),m))
                self.move(piece, m)
                if self.is_checkmate(team):
                    return (piece, m)
                self.move(piece, (pieceOldRow, pieceOldColumn))
                self._put_piece_in_square(oldPiece, (m[0], m[1]))
        else:
            return False

    def move(self, piece, newLocTuple):
        self._set_state(piece, newLocTuple)
        piece.move(newLocTuple)

    def _set_state(self, val, newLocTuple):
        tmpLst = [list(i) for i in self.state]
        tmpLst[val.row][val.column] = None
        tmpLst[newLocTuple[0]][newLocTuple[1]] = val
        self.state = tuple(tmpLst)

    def _put_piece_in_square(self, piece, locTuple):
        tmpLst = [list(i) for i in self.state]
        tmpLst[locTuple[0]][locTuple[1]] = piece
        self.state = tuple(tmpLst)


def get_opposing_team_char(piece):
    if isinstance(piece, Piece):
        team = piece.team
    elif isinstance(piece, str):
        team = piece
    else:
        raise Exception("Unknown type of argument ({0}) passed: {1}"
                .format(piece, piece.__class__))
    return 'd' if team == 'l' else 'l'


def dbprint(*args):
    if getattr(Config, 'debug', False) is True:
        print(args)
