
from abc import ABC
from typing import Generic

from chess.data import T


class AbstractInterface(Generic[T], ABC):
    def __init__(self, data: T, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: T = data

