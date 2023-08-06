
from abc import ABC

from chess.game.data import T
from chess.interface import AbstractInterface


class GameInterface(AbstractInterface[T], ABC):
    pass

