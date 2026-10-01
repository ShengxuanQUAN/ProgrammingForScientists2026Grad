#!/usr/bin/env python3
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import ete3

from distance_matrix import DistanceMatrix, load


@dataclass
class Node:
    """
    Represents a node in a phylogenetic tree.

    Attributes:
        num (int): Numeric identifier for the node (e.g., index in a tree list).
        age (float): Age (or height) of the node, typically half the distance between clusters.
        label (str): Label of the node, usually the species name for leaves.
        child1 (Self | None): The first child node, or None if this node is a leaf.
        child2 (Self | None): The second child node, or None if this node is a leaf.
    """

    num: int = 0
    age: float = 0.0
    label: str = ""
    child1: Self | None = None
    child2: Self | None = None

    def is_leaf(self) -> bool:
        """Return whether this node is a leaf (i.e., has no children)."""
        return self.child1 is None and self.child2 is None

    def count_leaves(self) -> int:
        """
        Recursively count the number of leaf nodes in the subtree rooted at this node.
        """
        if self.is_leaf():
            return 1
        leaves = 0
        if self.child1 is not None:
            leaves += self.child1.count_leaves()
        if self.child2 is not None:
            leaves += self.child2.count_leaves()
        return leaves

    def print(self, level=0):
        print("\t" * level, self.label, sep="")
        if self.child1 is not None:
            self.child1.print(level + 1)
        if self.child2 is not None:
            self.child2.print(level + 1)


Tree = list[Node]
"""A list of Node objects representing a phylogenetic tree structure."""


# === Student function to implement ===
def upgma(mtx: DistanceMatrix, species_names: list[str]) -> Tree:
    """
    Build a phylogenetic tree using the UPGMA algorithm.

    Given a distance matrix and species names, iteratively merges the closest
    clusters and updates the matrix using cluster-size–weighted averages.
    The resulting tree has `n` leaves (the species) and `n-1` internal nodes.

    Args:
        mtx (DistanceMatrix): Square symmetric matrix of pairwise distances.
        species_names (list[str]): Names of the species, in the same order as `mtx`.

    Returns:
        Tree: A list of `Node` objects representing the full UPGMA tree.
              Conventionally, the last node (index -1) is the root.
    """
    tree = initialize_tree(species_names)
    clusters = initialize_clusters(tree)
    for p in range(len(species_names), 2 * len(species_names) - 1):
        row, col, min_val = mtx.find_min_element()
        tree[p].age = min_val / 2
        tree[p].child1 = clusters[row]
        tree[p].child2 = clusters[col]
        cluster_size_1 = tree[p].child1.count_leaves()
        cluster_size_2 = tree[p].child2.count_leaves()
        mtx.add_row_col(row, col, cluster_size_1, cluster_size_2)
        mtx.del_rows_cols([row, col])
        clusters.append(tree[p])
        delete_clusters(clusters, row, col)
    return tree


# === Helper functions provided to students ===


def initialize_tree(species_names: list[str]) -> Tree:
    num_leaves = len(species_names)
    t: Tree = [Node(num=i) for i in range(2 * num_leaves - 1)]
    for i in range(len(t)):
        if i < num_leaves:
            t[i].label = species_names[i]
        else:
            t[i].label = f"ancestor_{i}"
    return t


def initialize_clusters(t: Tree) -> list[Node]:
    # the tree has 2n-1 total nodes;
    # return the first n nodes of the tree, corresponding to the leaves
    num_leaves = (len(t) + 1) // 2
    return [t[i] for i in range(num_leaves)]


def delete_clusters(clusters: list[Node], row: int, col: int) -> list[Node]:
    # remove merged cluster representatives at indices row and col
    indexes = sorted([row, col], reverse=True)
    for index in indexes:
        del clusters[index]
    return clusters


def build_ete3_tree(ete3_node: ete3.TreeNode, node: Node):
    if (c1 := node.child1) is not None:
        ete3_child1 = ete3_node.add_child(name=c1.label, dist=c1.age)
        build_ete3_tree(ete3_child1, c1)
    if (c2 := node.child2) is not None:
        ete3_child2 = ete3_node.add_child(name=c2.label, dist=c2.age)
        build_ete3_tree(ete3_child2, c2)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("matrix_file", type=Path)
    args = p.parse_args()

    base_name = args.matrix_file.stem

    mat, species = load(args.matrix_file)
    t = upgma(mat, species)
    root = t[-1]
    # print(t)
    assert root.count_leaves() == len(species)
    root.print()

    ete3_root = ete3.TreeNode(dist=root.age)
    build_ete3_tree(ete3_root, root)
    ts = ete3.TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_length = True
    ete3_root.render(f"{base_name}.pdf", tree_style=ts)
    ete3_root.write(outfile=f"{base_name}.newick")
