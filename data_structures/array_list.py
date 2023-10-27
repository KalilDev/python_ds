from typing import Iterable, Sized, Generic, TypeVar, Optional, List
E = TypeVar("E")


class ArrayList(Iterable[E], Sized, Generic[E]):
    elements: List[Optional[E]]
    length: int
    capacity: int

    def __init__(self, initial: Optional[Iterable[E]] = None):
        INITIAL_CAPACITY = 8
        self.elements = [None for i in range(INITIAL_CAPACITY)]
        self.length = 0
        self.capacity = INITIAL_CAPACITY
        if initial is not None:
            if isinstance(initial, Sized):
                self.reserve(len(initial))
            for e in initial:
                self.add(e)

    def reserve(self, desired_length: int) -> None:
        if desired_length <= self.capacity:
            return

        next_capacity = self.capacity
        while next_capacity < desired_length:
            next_capacity *= 2

        print("RESIZE FROM", self.capacity, next_capacity)

        new_elements = [self.elements[i] if i <
                        self.length else None for i in range(next_capacity)]
        self.capacity = next_capacity
        self.elements = new_elements

    def add(self, element: E) -> None:
        self.reserve(self.length + 1)
        self.elements[self.length] = element
        self.length += 1

    def remove_at(self, index: int) -> E:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        e = self.elements[index]
        for i in range(index, self.length - 1):
            self.elements[i] = self.elements[i+1]
        self.length -= 1
        return e

    def remove(self, element: E) -> bool:
        for i, e in enumerate(self.elements):
            if e == element:
                self.remove_at(i)
                return True
        return False

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterable[E]:
        for i, e in enumerate(self.elements):
            if i >= self.length:
                break
            yield e

    def __str__(self) -> str:
        out = "["
        out += ", ".join(map(str, self))
        out += "]"
        return out
