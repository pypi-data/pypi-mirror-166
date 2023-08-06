
from abc import ABC
from typing import Generic, TypeVar

from chess.move.data import MoveData
from chess.validator import AbstractValidator

T = TypeVar('T', bound=MoveData)

class MoveValidator(AbstractValidator[T], ABC):
    pass



