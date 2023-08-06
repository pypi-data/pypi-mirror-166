
from abc import ABC, abstractmethod

from chess.factory import AbstractFactory
from chess.move.data import T
from chess.offset import Offset
from chess.piece import Piece


class MoveFactory(AbstractFactory[T], ABC):
    @classmethod
    @abstractmethod
    def create(cls, piece: Piece, offset: Offset, *args, **kwargs) -> T:
        raise NotImplementedError

