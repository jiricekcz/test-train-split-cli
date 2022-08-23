from typing import Callable, Iterable
from common.interfaces.distance_matrix import IDistanceMatrix
from common.interfaces.splitter import ISplitter, ISplit
from sklearn.cluster import AgglomerativeClustering
import math
class Split(ISplit):
    def __init__(self, splits: Iterable[Iterable[int]]):
        self.splits_storage = splits

    def splits(self) -> Iterable[Iterable[int]]:
        return self.splits_storage

    def __str__(self):
        return str("\n".join(map(lambda x: f"[{', '.join(map(str, x))}]", self.splits())))

class AgglomerativeClusteringSplitter(ISplitter):
    clusterer: AgglomerativeClustering
    def __init__(self, splitCount: int) -> None:
        super().__init__()
        self.clusterer = AgglomerativeClustering(n_clusters=None, affinity="precomputed", compute_full_tree=True, linkage="single", compute_distances=True)
        self.splitCount = splitCount
        
    def calculateSplit(self, distances: IDistanceMatrix, distribution: "list[int]", splitCount = 0) -> list[ISplit]:
        groupSizes: list[int] = []
        distSum = sum(distribution)
        for relative in distribution:
            groupSizes.append(relative / distSum * distances.getMatrixSize())
        print(groupSizes)
        
        self.clusterer.n_clusters = 1
        self.clusterer.fit(distances.getNumpyNDArray())
        n_samples = len(self.clusterer.labels_)
        tree = ClusterTree(n_samples)
        for i, children in enumerate(self.clusterer.children_):
            tree.addParent(i + n_samples, children, distances.rawDistanceToDistance(self.clusterer.distances_[i]))


        # Distribute the samples among groups (not optimal solution)

        # A greedy distribution algorithm running in O(len(groupSums) * len(nums)) time.
        # Algortihm minimizes the distribution distance function at each step. Distribution distance function is in the following form: (targetSums, currentSums, currentOperatingIndex, valueToAddToThatIndex) -> distance
        def split(groupSums: list[float], subgroups: list[int], distributionDistance: Callable[[list[float], list[float], int, float], int]) -> list[int]:
            nums = [ListElement(x, i) for i, x in enumerate(subgroups)]
            nums.sort(key=lambda x: x.value, reverse=True)
            groups: list[list[ListElement]] = [[] for _ in groupSums] 
            def groupSum(group: "list[ListElement]") -> float:
                return sum(map(lambda x: x.value, group))
            for _, num in enumerate(nums):
                bestIndex = None
                bestValue = math.inf
                for j, _ in enumerate(groupSums):
                    value = distributionDistance(groupSums, list(map(groupSum, groups)), j, num.value)
                    if value < bestValue:
                        bestValue = value
                        bestIndex = j
                groups[bestIndex].append(num)
                print([list(map(str, group)) for group in groups])
            return groups
            
        def totalDistanceSquared(targetSums: list[float], currentSum: list[float], currentIndex: int, value: float) -> float:
            total = 0
            for i, targetSum in enumerate(targetSums):
                if i == currentIndex:
                    total += (targetSum - currentSum[i] - value)**2
                else:
                    total += (targetSum - currentSum[i])**2
            return total

        groups = split([2, 3, 5], [1,2,4,3], totalDistanceSquared)

        print([list(map(str, group)) for group in groups])
        for i in range(splitCount):
            pass

class ListElement:
    def __init__(self, value, index: int):
        self.value = value
        self.index = index
    def __str__(self) -> str:
        return f"Element<{self.index}, {'{0:.3f}'.format(self.value)}>"

        
class TreeNode:
    def __init__(self, id: int, children: list, depth: int):
        self.id = id
        self.children = children
        self.parent = None
        self.depth = depth
    
    def absoluteChildCount(self) -> int:
        return sum(map(lambda x: x.absoluteChildCount(), self.children)) + len(self.children)

    def __str__(self) -> str:
        return f"Node<{self.id}, {'{0:.3f}'.format(self.depth)}>"
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