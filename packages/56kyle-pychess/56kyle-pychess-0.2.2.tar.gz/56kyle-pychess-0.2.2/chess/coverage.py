
from dataclasses import dataclass, field
from typing import Set

from chess.position import Position


@dataclass(frozen=True)
class Coverage:
    positions: Set[Position] = field(default_factory=set)


