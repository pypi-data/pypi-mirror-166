
from dataclasses import dataclass

from .color import Color
from .position import Position


@dataclass(frozen=True)
class Piece:
    position: Position
    color: Color = Color.WHITE
    name: str = ''
    letter: str = ''
    value: int = 0
    symbol: str = ''
    html_decimal: str = ''
    html_hex: str = ''
    has_moved: bool = False

@dataclass(frozen=True)
class WhitePiece(Piece):
    color: Color = Color.WHITE

@dataclass(frozen=True)
class BlackPiece(Piece):
    color: Color = Color.BLACK


@dataclass(frozen=True)
class Pawn(Piece):
    name: str = 'Pawn'
    letter: str = 'P'
    value: int = 1

@dataclass(frozen=True)
class WhitePawn(Pawn, WhitePiece):
    symbol: str = '\u2659'
    html_decimal: str = '&#9817;'
    html_hex: str = '&#x2659;'

@dataclass(frozen=True)
class BlackPawn(Pawn, BlackPiece):
    symbol: str = '\u265F'
    html_decimal: str = '&#9823;'
    html_hex: str = '&#x265F;'


@dataclass(frozen=True)
class Knight(Piece):
    name: str = 'Knight'
    letter: str = 'N'
    value: int = 3

@dataclass(frozen=True)
class WhiteKnight(Knight, WhitePiece):
    symbol: str = '\u2658'
    html_decimal: str = '&#9816;'
    html_hex: str = '&#x2658;'

@dataclass(frozen=True)
class BlackKnight(Knight, BlackPiece):
    symbol: str = '\u265E'
    html_decimal: str = '&#9822;'
    html_hex: str = '&#x265E;'


@dataclass(frozen=True)
class Bishop(Piece):
    name: str = 'Bishop'
    letter: str = 'B'
    value: int = 3

@dataclass(frozen=True)
class WhiteBishop(Bishop, WhitePiece):
    symbol: str = '\u2657'
    html_decimal: str = '&#9815;'
    html_hex: str = '&#x2657;'

@dataclass(frozen=True)
class BlackBishop(Bishop, BlackPiece):
    symbol: str = '\u265D'
    html_decimal: str = '&#9821;'
    html_hex: str = '&#x265D;'


@dataclass(frozen=True)
class Rook(Piece):
    name: str = 'Rook'
    letter: str = 'R'
    value: int = 5

@dataclass(frozen=True)
class WhiteRook(Rook, WhitePiece):
    symbol: str = '\u2656'
    html_decimal: str = '&#9814;'
    html_hex: str = '&#x2656;'

@dataclass(frozen=True)
class BlackRook(Rook, BlackPiece):
    symbol: str = '\u265C'
    html_decimal: str = '&#9820;'
    html_hex: str = '&#x265C;'


@dataclass(frozen=True)
class Queen(Piece):
    name: str = 'Queen'
    letter: str = 'Q'
    value: int = 9

@dataclass(frozen=True)
class WhiteQueen(Queen, WhitePiece):
    symbol: str = '\u2655'
    html_decimal: str = '&#9813;'
    html_hex: str = '&#x2655;'

@dataclass(frozen=True)
class BlackQueen(Queen, BlackPiece):
    symbol: str = '\u265B'
    html_decimal: str = '&#9819;'
    html_hex: str = '&#x265B;'


@dataclass(frozen=True)
class King(Piece):
    name: str = 'King'
    letter: str = 'K'
    value: int = 0

@dataclass(frozen=True)
class WhiteKing(King, WhitePiece):
    symbol: str = '\u2654'
    html_decimal: str = '&#9812;'
    html_hex: str = '&#x2654;'

@dataclass(frozen=True)
class BlackKing(King, BlackPiece):
    symbol: str = '\u265A'
    html_decimal: str = '&#9818;'
    html_hex: str = '&#x265A;'

