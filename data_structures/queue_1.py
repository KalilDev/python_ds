from typing import Generic, Iterable, Optional, Sized, TypeVar

from data_structures.linked_list import LinkedList


E = TypeVar("E")


class Queue(Sized, Generic[E]):
    _storage: LinkedList[E]

    def __init__(self, initial: Optional[Iterable[E]] = None) -> None:
        super().__init__()
        self._storage = LinkedList(initial)

    def enqueue(self, e: E) -> None:
        self._storage.append(e)

    def peek(self, i: int = 0) -> Optional[E]:
        if len(self._storage) == 0:
            return None
        if len(self._storage) <= i:
            return None

        return self._storage.at(i)

    def dequeue(self) -> Optional[E]:
        return self._storage.remove_first()

    def __len__(self) -> int:
        return len(self._storage)
