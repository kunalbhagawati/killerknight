#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import sys

from core.components.board import Board
from core.config import Config

if __name__ == "__main__":
    sys.argv.pop(0)
    if '--debug' in sys.argv:
        Config.debug = True
        print(True)

    b = Board()
    print()
    print("isWhiteInCheck: {0}\n".format(b.is_white_in_check()))
    print("isWhiteInCheckMate: {0}\n".format(b.is_white_in_checkmate()))
    print("canBlackCheckMateInOneMove: {0}\n"
            .format(b.can_black_checkmate_in_one_move()))
    print("makeBlackCheckmateMove: {0}\n"
            .format(b.can_black_checkmate_in_one_move()))
    print("board string:")
    b.print_broard()
    print()
