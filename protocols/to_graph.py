from typing import Protocol
from graphviz import Digraph


class ToGraphable(Protocol):
    def to_digraph(self) -> Digraph: ...
