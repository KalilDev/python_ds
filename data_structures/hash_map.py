from typing import Generic, Mapping, Optional, Iterable, Tuple, TypeVar, Iterator

from data_structures.hash_table import HashTable, HashTableEntry

from protocols.hashable_and_equatable import HashableAndEquatable

K = TypeVar("K", bound=HashableAndEquatable)
V = TypeVar("V")


class HashMapEntry(HashTableEntry["HashMapEntry[K, V]", K], Generic[K, V]):
    def __init__(self, key: Optional[K] = None, value: Optional[V] = None):
        super().__init__(key)
        self.value = value

    value: Optional[V]

    def _label(self) -> str:
        return "{}" if self.key is None else "{" + str(self.key) + ": " + str(self.value)+"}"


class HashMap(HashTable[HashMapEntry, K], Iterable[K]):
    def create_empty_entry(self) -> HashMapEntry[K, V]:
        return HashMapEntry()

    def __init__(self, initial: Optional[Iterable[Tuple[K, V]] | Mapping[K, V]] = None) -> None:
        super().__init__()
        if initial is not None:
            self.reserve(len(initial))
            for e in initial:
                if isinstance(e, Tuple):
                    k, v = e
                    self[k] = v
                else:
                    k = e
                    v = initial[k]
                    self[k] = v

    def __setitem__(self, k: K, v: V) -> None:
        self.insert_entry(HashMapEntry(k, v))

    def __getitem__(self, k: K) -> Optional[V]:
        entry = self.find_entry(k)
        if entry is None:
            return None
        return entry.value

    def __contains__(self, k: K) -> bool:
        return self.find_entry(k) is not None

    def __iter__(self) -> Iterable[K]:
        for e in self.get_entries():
            if (e.key is not None):
                yield e.key

    def __str__(self) -> str:
        out = "{"
        out += ", ".join(map(lambda k: f"{k}: {self[k]}", self))
        out += "}"
        return out
