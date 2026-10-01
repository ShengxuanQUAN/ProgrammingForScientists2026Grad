#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Self


@dataclass
class Node:
    name: str
    left_child: Self | None = None
    right_child: Self | None = None

    def print(self, level=0):
        print("\t" * level, self.name, sep="")
        if self.left_child is not None:
            self.left_child.print(level + 1)
        if self.right_child is not None:
            self.right_child.print(level + 1)


leaves = [Node(f"leaf_{i}") for i in range(8)]
i1 = Node("i1", left_child=leaves[0], right_child=leaves[1])
i2 = Node("i2", left_child=leaves[2], right_child=leaves[3])
i3 = Node("i3", left_child=i2, right_child=leaves[4])
i4 = Node("i4", left_child=leaves[5], right_child=leaves[6])
i5 = Node("i5", left_child=i3, right_child=i4)
i6 = Node("i6", left_child=i5, right_child=leaves[7])
i7 = Node("i7", left_child=i1, right_child=i6)

i7.print()


def count_leaves(node: Node) -> int:
    if node.left_child is None or node.right_child is None:
        # not handling case in which only one child is None
        return 1
    else:
        return count_leaves(node.left_child) + count_leaves(node.right_child)


print(count_leaves(i7))
print(count_leaves(i3))


def count_leaves_iterative(node: Node) -> int:
    leaves = 0
    stack = [node]
    while stack:
        curr_node = stack.pop()
        if curr_node.left_child is None or curr_node.right_child is None:
            leaves += 1
        else:
            stack.append(curr_node.left_child)
            stack.append(curr_node.right_child)
    return leaves


print(count_leaves_iterative(i7))
