
from typing import Generic, Protocol, TypeVar


HashableAndEquatableSelf = TypeVar(
    "HashableAndEquatableSelf", bound="HashableAndEquatable")


class HashableAndEquatable(Protocol, Generic[HashableAndEquatableSelf]):
    def __hash__(self) -> int: ...
    def __eq__(self, other: HashableAndEquatableSelf) -> bool: ...
