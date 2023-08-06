
from abc import ABC
from dataclasses import dataclass
from typing import TypeVar

from chess.offset import Offset
from chess.piece import Piece
from chess.data import AbstractData


@dataclass(frozen=True)
class MoveData(AbstractData, ABC):
    piece: Piece
    offset: Offset


T = TypeVar('T', bound=MoveData)
