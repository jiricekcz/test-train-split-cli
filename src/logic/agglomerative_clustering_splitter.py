from random import random
from typing import Iterable
from common.interfaces.distance_matrix import IDistanceMatrix
from common.interfaces.splitter import ISplitter, ISplit
from sklearn.cluster import AgglomerativeClustering

class Split(ISplit):
    def __init__(self, splits: Iterable[Iterable[int]]):
        self.splits_storage = splits

    def splits(self) -> Iterable[Iterable[int]]:
        return self.splits_storage

    def __str__(self):
        return str("\n".join(map(lambda x: f"[{', '.join(map(str, x))}]", self.splits())))

class AgglomerativeClusteringSplitter(ISplitter):
    clusterer: AgglomerativeClustering
    def __init__(self) -> None:
        super().__init__()
        self.clusterer = AgglomerativeClustering(n_clusters=None, affinity="precomputed", compute_full_tree=True, linkage="single", compute_distances=True)
        
    def calculateSplit(self, distances: IDistanceMatrix, distribution: "list[int]") -> ISplit:
        

        self.clusterer.n_clusters = len(distribution)
        self.clusterer.fit(distances.getNumpyNDArray())
        print(distances.getMatrixSize())
        print(self.clusterer.labels_)
        print(self.clusterer.children_)
        n_samples = len(self.clusterer.labels_)
        tree = ClusterTree(n_samples)
        for i, children in enumerate(self.clusterer.children_):
            tree.addParent(i + n_samples, children, distances.self.clusterer.distances_[i]))
        print(list(map(str, tree.getRoots())))
        
class TreeNode:
    def __init__(self, id: int, children: list, depth: int):
        self.id = id
        self.children = children
        self.parent = None
        self.depth = depth
    def __str__(self) -> str:
        return f"Node<{self.id}, {self.depth}>"
class ClusterTree:
    nodes: list[TreeNode] = []
    def __init__(self, leafCount: int):
        for i in range(leafCount):
            self.nodes.append(TreeNode(i, [], 0))
    def addParent(self, id: int, childrenIds: list[int], depth: int) -> TreeNode:
        children = map(lambda x: self.nodes[x], childrenIds)
        node = TreeNode(id, children, depth)
        self.nodes.append(node)
        for child in children:
            child.parent = node
        return node
    def getRoots(self) -> list[TreeNode]:
        return list(filter(lambda x: x.parent == None, self.nodes))