
from abc import ABC
from dataclasses import dataclass
from typing import TypeVar

from chess.data import AbstractData


@dataclass(frozen=True)
class GameData(AbstractData, ABC):
    pass


T = TypeVar('T', bound=GameData)

