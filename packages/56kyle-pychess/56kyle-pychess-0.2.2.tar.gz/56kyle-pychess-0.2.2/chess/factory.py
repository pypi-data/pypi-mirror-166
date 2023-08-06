
from abc import ABC, abstractmethod
from typing import Generic

from chess.data import T


class AbstractFactory(Generic[T], ABC):
    def __init__(self, data: T, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: T = data

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> T:
        raise NotImplementedError

