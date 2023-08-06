
from abc import ABC
from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True)
class AbstractData(ABC):
    pass


T = TypeVar('T', bound=AbstractData)

