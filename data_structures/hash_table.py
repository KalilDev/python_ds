from typing import TypeVar, Iterable, Sized, Optional, Generic, List

from graphviz import Digraph
from protocols.hashable_and_equatable import HashableAndEquatable
from data_structures.linked_list import IntrusiveLinkedListNode

K = TypeVar("K", bound=HashableAndEquatable)
HashTableEntrySelf = TypeVar("HashTableEntrySelf", bound="HashTableEntry")


class HashTableEntry(IntrusiveLinkedListNode[HashTableEntrySelf], Generic[HashTableEntrySelf, K]):
    key: Optional[K]

    def __init__(self, key: Optional[K] = None):
        self.key = key
        super().__init__()

    def _label(self) -> str:
        return str(self)


class HashTable(Generic[HashTableEntrySelf, K], Sized):
    entries: List[HashTableEntrySelf]
    capacity: int
    length: int

    def create_empty_entry(self) -> HashTableEntrySelf:
        pass

    def find_entry(self, key: K) -> Optional[HashTableEntrySelf]:
        key_hash = hash(key)
        index = key_hash % self.capacity
        first_entry = self.entries[index]
        for entry in first_entry:
            if entry.key == key:
                return entry
        return None

    def remove_entry(self, key: K) -> bool:
        key_hash = hash(key)
        index = key_hash % self.capacity
        first_entry = self.entries[index]
        previous = first_entry
        for entry in first_entry:
            if entry.key == key:
                if entry is first_entry:
                    if entry.next is not None:
                        self.entries[index] = entry.next
                        self.length -= 1
                        return True
                    self.entries[index] = self.create_empty_entry()
                    self.length -= 1
                    return True
                previous.next = entry.next
                self.length -= 1
                return True
            previous = entry
        return False

    def rehash_entry(self, entry: HashTableEntrySelf) -> None:
        if (entry.next is None):
            if (entry.key is not None):
                self.insert_entry(entry)
                return
            return
        self.rehash_entry(entry.next)
        entry.next = None
        if (entry.key is not None):
            self.insert_entry(entry)

    def rehash(self, old_entries: List[HashTableEntrySelf]) -> None:
        for initial_entry in old_entries:
            self.rehash_entry(initial_entry)

    def reserve(self, length: int) -> None:
        if (length <= self.capacity / 2):
            return
        new_capacity = self.capacity
        while length > new_capacity / 2:
            new_capacity *= 2

        old_entries = self.entries
        self.length = 0
        self.entries = [self.create_empty_entry()
                        for i in range(new_capacity)]
        self.capacity = new_capacity
        self.rehash(old_entries)

    def insert_entry(self, entry: HashTableEntrySelf) -> None:
        assert (entry.next is None)
        self.reserve(self.length + 1)
        key = entry.key
        key_hash = hash(key)
        index = key_hash % self.capacity
        first_entry = self.entries[index]
        if (first_entry.key is None and first_entry.next is None):
            self.entries[index] = entry
            self.length += 1
            return

        if first_entry.key == entry.key:
            self.entries[index] = entry
            entry.next = first_entry.next
            return
        last = first_entry
        for next_entry in first_entry:
            if next_entry.key == entry.key:
                last.next = entry
                entry.next = next_entry.next
                return
            last = next_entry
        last.next = entry
        self.length += 1

    def get_entries(self) -> Iterable[HashTableEntrySelf]:
        for initial_entry in self.entries:
            for e in initial_entry:
                yield e

    def __len__(self) -> int:
        return self.length

    def __init__(self) -> None:
        INITIAL_HASH_TABLE_LENGTH = 4
        self.entries = [self.create_empty_entry()
                        for i in range(INITIAL_HASH_TABLE_LENGTH)]
        self.capacity = INITIAL_HASH_TABLE_LENGTH
        self.length = 0
        super().__init__()

    def to_digraph(self) -> Digraph:
        dot = Digraph()
        dot.node("root", label="Root")
        for i, e in enumerate(self.entries):
            entry_node_id = f"root-{i}"
            dot.node(entry_node_id, label=e._label())
            dot.edge("root", entry_node_id)
            previous_entry_node_id = entry_node_id
            is_first = True
            for i, sub_e in enumerate(e):
                if is_first:
                    is_first = False
                    continue
                entry_node_id = previous_entry_node_id + f'-{i}'
                dot.node(entry_node_id, label=sub_e._label())
                dot.edge(previous_entry_node_id, entry_node_id)
                previous_entry_node_id = entry_node_id
        return dot
