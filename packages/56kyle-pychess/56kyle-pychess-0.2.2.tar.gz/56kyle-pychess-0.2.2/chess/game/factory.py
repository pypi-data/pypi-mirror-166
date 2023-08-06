from abc import ABC

from chess.game.data import T
from chess.factory import AbstractFactory


class GameFactory(AbstractFactory[T], ABC):
    pass


