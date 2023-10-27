from typing import Any, TypeVar, Iterable, Sized, Optional, Generic

from graphviz import Digraph

IntrusiveLinkedListNodeSelf = TypeVar(
    "IntrusiveLinkedListNodeSelf", bound="IntrusiveLinkedListNode")


class IntrusiveLinkedListNode(Generic[IntrusiveLinkedListNodeSelf], Iterable[IntrusiveLinkedListNodeSelf]):
    next: Optional[IntrusiveLinkedListNodeSelf]

    def __init__(self, next: Optional[IntrusiveLinkedListNodeSelf] = None):
        self.next = next

    def __iter__(self):
        curr = self
        while curr is not None:
            yield curr
            curr = curr.next

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "next":
            assert (__value is not self)
        return super().__setattr__(__name, __value)


E = TypeVar("E")


class LinkedListNode(IntrusiveLinkedListNode["LinkedListNode[E]"], Generic[E]):
    value: E

    def __init__(self, value: E):
        self.value = value
        super().__init__()


E = TypeVar("E")


class LinkedList(Generic[E], Sized, Iterable[E]):
    _first: Optional[LinkedListNode[E]]
    _last: Optional[LinkedListNode[E]]
    _size: int

    def __init__(self, initial: Optional[Iterable[E]] = None):
        self._first = None
        self._last = None
        self._size = 0
        if initial is not None:
            for e in initial:
                self.append(e)

    def __len__(self):
        return self._size

    def __iter__(self):
        if self._first is not None:
            for node in self._first:
                yield node.value

    def append(self, el: E) -> None:
        self._size += 1
        node = LinkedListNode(el)
        if self._last is None:
            self._first = self._last = node
            return
        self._last.next = node
        self._last = node

    def prepend(self, el: E) -> None:
        self._size += 1
        node = LinkedListNode(el)
        if self._last is None:
            self._first = self._last = node
            return
        node.next = self._first
        self._first = node

    def remove(self, el: E) -> Optional[E]:
        if self._first is None:
            return None
        if self._first.value == el:
            if self._size == 1:
                self._size = 0
                self._first = None
                self._last = None
                return el
            self._size -= 1
            self._first = self._first.next
            return
        prev = self._first
        curr = prev.next
        while curr is not None and curr.value != el:
            prev = curr
            curr = curr.next
        if curr is None:
            return None
        if curr is self._last:
            self._last = prev
            self._size -= 1
            return el
        next = curr.next
        prev.next = next
        self._size -= 1
        return el

    def remove_first(self) -> Optional[E]:
        if self._first is None:
            return None
        e = self._first.value
        if self._size == 1:
            self._first = None
            self._last = None
            self._size -= 1
            return e
        self._first = self._first.next
        self._size -= 1
        return e

    def at(self, i: int) -> E:
        if i <= 0:
            i = self._size + i
        if i >= self._size:
            raise IndexError(i)

        if i == 0:
            return self.first()
        if i == self._size - 1:
            return self.last()

        for ei, e in enumerate(self):
            if ei == i:
                return e

        raise IndexError(i)

    def __str__(self) -> str:
        out = "["
        out += ", ".join(map(str, self))
        out += "]"
        return out

    def first(self) -> Optional[E]:
        if self._first is None:
            return None
        return self._first.value

    def last(self) -> Optional[E]:
        if self._last is None:
            return None
        return self._last.value

    def to_digraph(self) -> Digraph:
        dot = Digraph()
        if self._last is None:
            return dot
        for i, e in enumerate(self._first):
            dot.node(name=f"{i}", label=f"{e.value}")
        for i, e in enumerate(self._first):
            if e.next is not None:
                dot.edge(f"{i}", f"{i+1}")
        return dot
