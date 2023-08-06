
from dataclasses import dataclass

from chess.color import Color
from chess.side import Side


@dataclass(frozen=True)
class CastleRight:
    color: Color
    side: Side


