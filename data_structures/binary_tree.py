from typing import TypeVar, Optional, Generic

E = TypeVar("E")
BinaryTreeNodeSelf = TypeVar("BinaryTreeNodeSelf", bound="BinaryTreeNode")


class BinaryTreeNode(Generic[BinaryTreeNodeSelf, E]):
    value: E
    left: Optional[BinaryTreeNodeSelf]
    right: Optional[BinaryTreeNodeSelf]

    def __init__(self, value: E,
                 left: Optional[BinaryTreeNodeSelf] = None,
                 right: Optional[BinaryTreeNodeSelf] = None):
        self.value = value
        self.left = left
        self.right = right

    def _label(self) -> str:
        return str(self)


ParentLinkedBinaryTreeNodeSelf = TypeVar(
    "ParentLinkedBinaryTreeNodeSelf", bound="ParentLinkedBinaryTreeNode")


class ParentLinkedBinaryTreeNode(BinaryTreeNode[ParentLinkedBinaryTreeNodeSelf, E], Generic[ParentLinkedBinaryTreeNodeSelf, E]):
    parent: Optional[ParentLinkedBinaryTreeNodeSelf]

    def __init__(self, value: E,
                 parent: Optional[ParentLinkedBinaryTreeNodeSelf] = None,
                 left: Optional[BinaryTreeNodeSelf] = None,
                 right: Optional[BinaryTreeNodeSelf] = None):
        self.parent = parent
        super().__init__(value, left, right)
