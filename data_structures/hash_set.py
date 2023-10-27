from typing import Generic, Optional, Iterable, TypeVar
from data_structures.hash_table import HashTable, HashTableEntry

from protocols.hashable_and_equatable import HashableAndEquatable

E = TypeVar("E", bound=HashableAndEquatable)


class HashSetEntry(HashTableEntry["HashSetEntry[E]", E], Generic[E]):
    def __init__(self, key: Optional[E] = None):
        super().__init__(key)

    def _label(self) -> str:
        return "{}" if self.key is None else "{" + str(self.key)+"}"


class HashSet(HashTable[HashSetEntry, E], Iterable[E]):
    def create_empty_entry(self) -> HashSetEntry[E]:
        return HashSetEntry()

    def __init__(self, initial: Optional[Iterable[E]] = None) -> None:
        super().__init__()
        if initial is not None:
            self.reserve(len(initial))
            for e in initial:
                self.add(e)

    def add(self, n: E) -> None:
        self.insert_entry(HashSetEntry(n))

    def contains(self, n: E) -> bool:
        return self.find_entry(n) is not None

    def __delitem__(self, n: E) -> None:
        self.remove_entry(n)

    def __getitem__(self, n: E) -> Optional[E]:
        return n if self.contains(n) else None

    def __contains__(self, n: E) -> bool:
        return self.contains(n)

    def __iter__(self) -> Iterable[E]:
        for e in self.get_entries():
            if e.key is not None:
                yield e.key

    def __add__(self, other_set: "HashSet[E]") -> "HashSet[E]":
        out = HashSet()
        out.reserve(len(self) + len(other_set))
        for a in self:
            out.add(a)
        for b in other_set:
            out.add(b)
        return out

    def __or__(self, other_set: "HashSet[E]") -> "HashSet[E]":
        return self + other_set

    def __sub__(self, other_set: "HashSet[E]") -> "HashSet[E]":
        out = HashSet()
        out.reserve(len(self) - len(other_set))
        for a in self:
            if a not in other_set:
                out.add(a)
        return out

    def __and__(self, other_set: "HashSet[E]") -> "HashSet[E]":
        out = HashSet()
        for a in self:
            if a in other_set:
                out.add(a)
        return out

    def __str__(self):
        out = "{"
        out += ", ".join(map(str, self))
        out += "}"
        return out
