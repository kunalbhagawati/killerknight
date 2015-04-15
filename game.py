#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from core.components.board import Board


if __name__ == "__main__":
    b = Board()
    print()
    print("isWhiteInCheck: {0}\n".format(b.is_white_in_check()))
    print("board string:")
    b.print_broard()
    print()
