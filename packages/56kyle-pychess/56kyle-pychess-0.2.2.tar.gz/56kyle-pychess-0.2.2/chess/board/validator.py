
from abc import ABC

from chess.board.data import T
from chess.validator import AbstractValidator


class BoardValidator(AbstractValidator[T], ABC):
    pass


