
from abc import ABC, abstractmethod
from typing import Generic

from chess.data import T


class AbstractValidator(Generic[T], ABC):
    def __init__(self, data: T, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: T = data

    @classmethod
    @abstractmethod
    def is_valid(cls, data: T, *args, **kwargs) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def validate(cls, data: T, *args, **kwargs) -> bool:
        raise NotImplementedError

