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
        for col in readRows:
            col = col.split("|")
            col.pop(0)
            col.pop(len(col)-1)
            colVal = [self._get_peice_from_string(i) for i in col]
            self.state += (colVal, )

    def _get_string(self):
        root = (ospath.dirname(
            ospath.dirname(
                ospath.dirname(
                    ospath.abspath(__file__)))))
        with open('{0}/usr/input.txt'.format(root), "r") as f:
            readData = f.read()
        return readData

    def _get_peice_from_string(self, string):
        if string == '  ':
            return None
        else:
            peiceTypes = {
                'k': King,
                'n': Knight
            }
            team = string[1]
            return peiceTypes[string[0]](team)

    def _get_state(self, asString=0):
        if not asString:
            return self.state
        else:
            string = ''
            for row in self.state:
                string += "|"
                for cell in row:
                    if cell is None:
                        string += '  '
                    else:
                        # TODO do below by dict
                        if isinstance(cell, King):
                            string += 'k'
                        elif isinstance(cell, Knight):
                            string += 'n'
                        string += cell.team
                    string += "|"
                string += "\n"
            return string

    def _print_broard(self):
        print(self._get_state(asString=1))
