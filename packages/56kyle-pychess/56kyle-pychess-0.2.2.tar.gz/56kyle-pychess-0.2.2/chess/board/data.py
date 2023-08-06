from abc import ABC
from dataclasses import dataclass
from typing import Set, TypeVar

from chess.castle_right import CastleRight
from chess.position import Position
from chess.piece import Piece
from chess.data import AbstractData


@dataclass(frozen=True)
class BoardData(AbstractData, ABC):
    pieces: Set[Piece]
    castling_rights: Set[CastleRight]
    en_passant_target_position: Position | None
    half_move_draw_clock: int
    full_move_number: int
    width: int
    height: int


T = TypeVar('T', bound=BoardData)

