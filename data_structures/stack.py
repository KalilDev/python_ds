from math import pi
from typing import Callable, Generic, Iterable, Optional, Reversible, Sized, TypeVar

from data_structures.linked_list import LinkedList


E = TypeVar("E")


class Stack(Sized, Generic[E]):
    _storage: LinkedList[E]

    def __init__(self, initial: Optional[Reversible[E]] = None) -> None:
        super().__init__()
        if initial is not None:
            self._storage = LinkedList(reversed(initial))
        else:
            self._storage = LinkedList()

    def push(self, e: E) -> None:
        self._storage.prepend(e)

    def peek(self, i: int = 0) -> Optional[E]:
        if len(self._storage) <= i:
            return None

        return self._storage.at(i)

    def pop(self) -> Optional[E]:
        return self._storage.remove_first()

    def __len__(self) -> int:
        return len(self._storage)
