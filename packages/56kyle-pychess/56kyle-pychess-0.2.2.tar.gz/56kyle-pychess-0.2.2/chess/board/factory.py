
from abc import ABC, abstractmethod
from typing import Set

from chess.board.data import T
from chess.castle_right import CastleRight
from chess.factory import AbstractFactory
from chess.piece import Piece
from chess.position import Position


class BoardFactory(AbstractFactory[T], ABC):
    @classmethod
    @abstractmethod
    def create(cls, pieces: Set[Piece],
               castling_rights: Set[CastleRight],
               en_passant_target_position: Position | None,
               half_move_draw_clock: int,
               full_move_number: int,
               width: int,
               height: int) -> T:
        raise NotImplementedError
