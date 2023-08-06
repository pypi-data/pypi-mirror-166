
from abc import ABC
from typing import TypeVar

from chess.move.data import MoveData
from chess.interface import AbstractInterface

T = TypeVar('T', bound=MoveData)

class MoveInterface(AbstractInterface[T], ABC):
    pass


