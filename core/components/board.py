#!/usr/bin/env python3

from os import path as ospath
from .pieces import Knight, King


class Board:

    def __init__(self):
        self._construct_board()

    def _construct_board(self):
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
        return True if self._is_hunter_watching(self.kl) else False

    # def _get_possible_moves(self, piece):
    #     if isinstance(piece, Knight):
    #         rows =

    def _is_hunter_watching(self, piece):
        possibleKillZones = self._get_killzones(piece)

        hunters = ()
        # TODO trivial solution. Make better
        for kz in possibleKillZones:
            if self.state[kz[0]][kz[1]] is not None:
                hunters += (self.state[kz[0]][kz[1]], )

        return hunters or False

    def _get_killzones(self, piece):
        killzones = set()
        for p in self.piecesInBoard[get_opposing_team_char(piece)]:
            killzones.update((piece.row+move[0], piece.column+move[1])
                    for move in p.baseMoves
                    if piece.row+move[0] > 0 and piece.column+move[1] > 0)
        return killzones


def get_opposing_team_char(piece):
    return 'd' if piece.team == 'l' else 'l'
