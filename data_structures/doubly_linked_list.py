from typing import Any, Iterator, TypeVar, Iterable, Sized, Optional, Generic, Reversible
from graphviz import Digraph

IntrusiveDoublyLinkedListNodeSelf = TypeVar(
    "IntrusiveDoublyLinkedListNodeSelf", bound="IntrusiveDoublyLinkedListNode")


class IntrusiveDoublyLinkedListNode(Generic[IntrusiveDoublyLinkedListNodeSelf], Reversible[IntrusiveDoublyLinkedListNodeSelf], Iterable[IntrusiveDoublyLinkedListNodeSelf]):
    previous: Optional[IntrusiveDoublyLinkedListNodeSelf]
    next: Optional[IntrusiveDoublyLinkedListNodeSelf]

    def __init__(self, previous: Optional[IntrusiveDoublyLinkedListNodeSelf] = None, next: Optional[IntrusiveDoublyLinkedListNodeSelf] = None):
        self.previous = previous
        self.next = next

    def __iter__(self):
        curr = self
        while curr is not None:
            yield curr
            curr = curr.next

    def __reversed__(self) -> Iterator[IntrusiveDoublyLinkedListNodeSelf]:
        curr = self
        while curr is not None:
            yield curr
            curr = curr.previous

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "next":
            assert (__value is not self)
        return super().__setattr__(__name, __value)


def link_two_nodes(left: IntrusiveDoublyLinkedListNode, right: IntrusiveDoublyLinkedListNode, override: bool = False) -> None:
    if not override:
        assert (left.next is None)
        assert (right.previous is None)
    left.next = right
    right.previous = left


def unlink_node_back(node: IntrusiveDoublyLinkedListNode) -> None:
    assert (node.previous is not None)
    node.previous = None


def unlink_node_front(node: IntrusiveDoublyLinkedListNode) -> None:
    assert (node.next is not None)
    node.next = None


def remove_node_in_between(left: IntrusiveDoublyLinkedListNode, center: IntrusiveDoublyLinkedListNode, right: IntrusiveDoublyLinkedListNode) -> None:
    assert (left.next is center)
    assert (center.next is right)
    assert (center.previous is left)
    assert (right.previous is center)
    center.next = None
    center.previous = None
    left.next = right
    right.previous = left


E = TypeVar("E")


class DoublyLinkedListNode(IntrusiveDoublyLinkedListNode["DoublyLinkedListNode[E]"], Generic[E]):
    value: E

    def __init__(self, value: E):
        self.value = value
        super().__init__()


E = TypeVar("E")


class DoublyLinkedList(Generic[E], Sized, Reversible[E], Iterable[E]):
    _first: Optional[DoublyLinkedListNode[E]]
    _last: Optional[DoublyLinkedListNode[E]]
    _size: int

    def __init__(self, initial: Optional[Iterable[E]] = None):
        self._first = None
        self._last = None
        self._size = 0
        if initial is not None:
            for e in initial:
                self.append(e)

    def __str__(self) -> str:
        out = "["
        out += ", ".join(map(str, self))
        out += "]"
        return out

    def __len__(self):
        return self._size

    def __iter__(self):
        if self._first is not None:
            for node in self._first:
                yield node.value

    def __reversed__(self) -> Iterator[E]:
        return map(lambda node: node.value, reversed(self._last))

    def append(self, el: E) -> None:
        self._size += 1
        node = DoublyLinkedListNode(el)
        if self._last is None:
            self._first = self._last = node
            return
        link_two_nodes(self._last, node)
        self._last = node

    def prepend(self, el: E) -> None:
        self._size += 1
        node = DoublyLinkedListNode(el)
        if self._last is None:
            self._first = self._last = node
            return
        link_two_nodes(node, self._first)
        self._first = node

    def remove_first(self) -> Optional[E]:
        if self._size == 0:
            return None
        e = self._first.value
        if self._size == 1:
            self._first = None
            self._last = None
            self._size -= 1
            return e
        self._first = self._first.next
        unlink_node_back(self._first)
        return e

    def remove_last(self) -> Optional[E]:
        if self._size == 0:
            return None
        e = self._last.value
        if self._size == 1:
            self._first = None
            self._last = None
            self._size -= 1
            return e
        self._last = self._last.previous
        unlink_node_front(self._last)
        return e

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
            unlink_node_back(self._first)
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
            unlink_node_front(self._last)
            self._size -= 1
            return el
        remove_node_in_between(prev, curr, curr.next)
        self._size -= 1
        return el

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
        out = ""
        if self._last is None:
            return dot
        for i, e in enumerate(self._first):
            dot.node(name=f"{i}", label=f"{e.value}")
        for i, e in enumerate(self._first):
            if e.next is not None:
                dot.edge(f"{i}", f"{i+1}")
                out += f"E({i}, {i+1})\n"
            if e.previous is not None:
                dot.edge(f"{i}", f"{i-1}")
                out += f"E({i}, {i-1})\n"
        return dot
