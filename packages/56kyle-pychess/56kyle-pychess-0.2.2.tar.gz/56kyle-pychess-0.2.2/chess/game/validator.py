
from abc import ABC

from chess.game.data import T
from chess.validator import AbstractValidator


class GameValidator(AbstractValidator[T], ABC):
    pass

