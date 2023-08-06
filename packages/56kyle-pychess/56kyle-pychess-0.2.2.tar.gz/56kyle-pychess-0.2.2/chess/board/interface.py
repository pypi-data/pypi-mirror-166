
from abc import ABC

from chess.board.data import T
from chess.interface import AbstractInterface


class BoardInterface(AbstractInterface[T], ABC):
    pass


