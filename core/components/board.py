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
        for i, col in enumerate(readRows):
            col = col.split("|")
            col.pop(0)
            col.pop(len(col)-1)
            colVal = ()
            self.piecesInBoard = set()
            for j, cell in enumerate(col):
                piece = self._get_piece_from_string(cell)
                piece.row = i
                piece.column = j
                self.piecesInBoard.add(piece.__class__)
                if isinstance(piece, King):
                    setattr(self, cell)
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
        return True if self._is_hunter_watching(self.kl) else return False

    def _get_possible_moves(self, piece):
        if isinstance(piece, Knight):
            rows = 

    def _is_hunter_watching(self, piece):
        possibleKillZones = _get_killzones(piece)

    def _get_killzones(self, piece):
        killzones = set()
        for p in self.piecesInBoard:
            if isinstance(p, Knight):
                killzones.update((
                    (piece.row+2, piece.column+1),
                    (piece.row+2, piece.column-1),
                    (piece.row-2, piece.column+1),
                    (piece.row-2, piece.column-1),
                    (piece.row+1, piece.column+2),
                    (piece.row+1, piece.column-2),
                    (piece.row-1, piece.column+2),
                    (piece.row-1, piece.column-2),
                ))
            if isinstance(k, King):
                killzones.update((
                    (piece.row-1, piece.column-1),
                    (piece.row-1, piece.column),
                    (piece.row-1, piece.column+1),

                    (piece.row, piece.column-1),
                    (piece.row, piece.column),
                    (piece.row, piece.column+1),

                    (piece.row+1, piece.column-1),
                    (piece.row+1, piece.column),
                    (piece.row+1, piece.column+1),
                ))

            for i in killzones