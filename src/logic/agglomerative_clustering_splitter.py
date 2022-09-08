from typing import Callable, Iterable
from common.interfaces.distance_matrix import IDistanceMatrix
from common.interfaces.splitter import ISplitter, ISplit
from sklearn.cluster import AgglomerativeClustering
import math
class Split(ISplit):
    def __init__(self, splits: Iterable[Iterable[int]], minimalDistanceBetweenSplits: float):
        self.splits_storage = splits
        self.minimalDistanceBetweenSplitsStorage = minimalDistanceBetweenSplits

    def splits(self) -> Iterable[Iterable[int]]:
        return self.splits_storage

    def minimalDistanceBetweenSplits(self) -> float:
        return self.minimalDistanceBetweenSplitsStorage

class AgglomerativeClusteringSplitter(ISplitter):
    clusterer: AgglomerativeClustering
    def __init__(self, headstartFactor: int) -> None:
        super().__init__()
        if headstartFactor > 100: raise ValueError("headstartFactor must be less than 100")
        if headstartFactor < 0: raise ValueError("headstartFactor must be greater than 0")
        if headstartFactor == 0: self.headstartFactor = None
        else: self.headstartFactor = 100 / headstartFactor
        self.clusterer = AgglomerativeClustering(n_clusters=None, affinity="precomputed", compute_full_tree=True, linkage="single", compute_distances=True)

    def calculateSplit(self, distances: IDistanceMatrix, distribution: "list[int]") -> Iterable[ISplit]:
        groupSizes: list[int] = [] # absolute group sizes calculated from distribution
        distSum = sum(distribution)
        for relative in distribution:
            groupSizes.append(relative / distSum * distances.getMatrixSize())
        
        self.clusterer.n_clusters = 1 # calculate full tree
        self.clusterer.fit(distances.getNumpyNDArray())
        n_samples = len(self.clusterer.labels_) 
        tree: ClusterTree = ClusterTree(n_samples)
        
        for i, children in enumerate(self.clusterer.children_):
            tree.addParent(i + n_samples, children, distances.rawDistanceToDistance(self.clusterer.distances_[i]))
        
        tree.freezeTree()

        # Distribute the samples among groups (not optimal solution)

        def groupSum(group: "list[ListElement]") -> float:
                return sum(map(lambda x: x.value, group))
        # A greedy distribution algorhithm running in O(len(groupSums) * len(nums)) time.
        # Algorhithm minimizes the distribution distance function at each step. Distribution distance function is in the following form: (targetSums, currentSums, currentOperatingIndex, valueToAddToThatIndex) -> distance
        def split(groupSums: "list[float]", subgroups: "list[int]", distributionDistance: "Callable[[list[float], list[float], int, float], int]") -> "list[list[ListElement]]":
            """
            Splits the subgroups into groups to approach the groupSums. Value of a given distrubution is determined by the distributionDistance function.
            """
            nums = [ListElement(x, i) for i, x in enumerate(subgroups)] # An array of ListElements, the index is the id of the subgroup later used to reference it, value is the size of the subgroup
            nums.sort(key=lambda x: x.value, reverse=True) # Sort the elements by value in descending order
            groups: list[list[ListElement]] = [[] for _ in groupSums]  # list of groups to be returned
            for num in nums: # Add each subgorup to a group, starting with the largest subgroup
                bestIndex = None
                bestValue = math.inf
                for j, _ in enumerate(groupSums): # Find the best group to add the subgroup to
                    value = distributionDistance(groupSums, list(map(groupSum, groups)), j, num.value)
                    if value < bestValue:
                        bestValue = value
                        bestIndex = j
                groups[bestIndex].append(num)
            return groups
            
        def totalDistanceSquared(targetSums: "list[float]", currentSum: "list[float]", currentIndex: int, value: float) -> float:
            """
            Calculates the total distance squared between the targetSums and the currentSums.
            """
            total = 0
            for i, targetSum in enumerate(targetSums):
                if i == currentIndex:
                    total += (targetSum - currentSum[i] - value)**2
                else:
                    total += (targetSum - currentSum[i])**2
            return total

        def totalRelativeDistanceSquared(targetSums: "list[float]", currentSum: "list[float]", currentIndex: int, value: float) -> float:
            """
            Calculates the total relative distance squared between the targetSums and the currentSums.
            """
            total = 0
            for i, targetSum in enumerate(targetSums):
                if i == currentIndex:
                    total += ((targetSum - currentSum[i] - value)/targetSum)**2
                else:
                    total += ((targetSum - currentSum[i])/targetSum)**2
            return total


        def totalRelativeDistanceSquaredWithBiasAgainstOverflow(targetSums: "list[float]", currentSum: "list[float]", currentIndex: int, value: float) -> float:
            """
            Calculates the total relative distance squared between the targetSums and the currentSums. Also, if the value would overflow, the distance is greatly increased.
            """
            total = 0
            for i, targetSum in enumerate(targetSums):
                if i == currentIndex:
                    relDist = ((targetSum - currentSum[i] - value)/targetSum)
                else:
                    relDist = ((targetSum - currentSum[i])/targetSum)
                if relDist < 0:
                    total += relDist**2 * 5
                else:
                    total += relDist**2
            return total
        def groupDistances(groups: "list[list[int]]", distances: IDistanceMatrix) -> "list[list[float]]":
            """
            Calculates a distance matrix between given groups. The distance between two groups is defined as the minimal distance between any two elements from the groups.
            """
            gDistances = [[1 for _ in range(len(groups))] for _ in range(len(groups))]
            for i in range(len(groups)):
                for j in range(i + 1, len(groups)):
                    minDist = 1
                    for x in groups[i]:
                        for y in groups[j]:
                            dist = distances.getDistance(x, y)
                            if dist < minDist:
                                minDist = dist
                    gDistances[i][j] = minDist
                    gDistances[j][i] = minDist
            return gDistances
        subgroups: list[TreeNode] = tree.getRoots()

        for i in range(distances.getMatrixSize()): # generates and yields splits
            subgroupsPopCount = [subgroup.absoluteChildCount() for subgroup in subgroups] # absolute subgroup sizes
            # Different split algorthims and value functions were in all testcases almost incosequential. With the nature of the data, it is expected for a large amount of size 1 subgroups to be created.
            groups = split(groupSizes, subgroupsPopCount, totalRelativeDistanceSquaredWithBiasAgainstOverflow) # distributes the subgroups among groups using the provided value function
            
            finalSplit: list[list[int]] = []
            for i, group in enumerate(groups): # transforms the groups of leafs of the tree into a list of lists of indices
                finalSplit.append([])
                for element in group:
                    finalSplit[i].extend([leaf.id for leaf in subgroups[element.index].leafs])
                pass
            
            gDistances = groupDistances(finalSplit, distances)
            minDistance = min([min(row) for row in gDistances])
            yield Split(finalSplit, minDistance)
            currentDistance = totalRelativeDistanceSquaredWithBiasAgainstOverflow(groupSizes, [len(group) for group in groups], 0, 0)
            if self.headstartFactor == None: steps = 1
            else: steps = int(currentDistance / len(groups) * distances.getMatrixSize() / (self.headstartFactor - 1) + 1)
            for _ in range(steps): # Splits the tree the calculated number of times, this is done more than once only to speed up the process. The number of steps is calculated based on the current distance between the groups and the headstart factor.
                maxIndex = None
                maxValue = 1
                for i, subgroup in enumerate(subgroups):
                    if maxValue > subgroup.depth and subgroup.absoluteChildCount() > 1:
                        maxValue = subgroup.depth
                        maxIndex = i
                if maxIndex == None:
                    break
                c1, c2 = subgroups[maxIndex].children
                subgroups[maxIndex] = c1
                subgroups.append(c2)



class ListElement:
    def __init__(self, value, index: int):
        self.value = value
        self.index = index
    def __repr__(self) -> str:
        return f"Element<{self.index}, {'{0:.3f}'.format(self.value)}>"

        
class TreeNode:
    children: "list[TreeNode]"
    def __init__(self, id: int, children: "list[TreeNode]", depth: int, isLeaf=False):
        self.id = id
        self.children = children
        self.parent = None
        self.depth = depth
        self.absoluteChildCountCache = None
        self.leafs: "list[TreeNode]" = []
        if isLeaf:
            self.leafs.append(self)
        else:
            for child in self.children:
                child.parent = self
                self.leafs.extend(child.leafs)
    def absoluteChildCount(self) -> int:
        if self.absoluteChildCountCache != None:
            return self.absoluteChildCountCache
        return len(self.leafs)

    def cacheAbsoluteChildCount(self) -> None:
        self.absoluteChildCountCache = self.absoluteChildCount()

    def __str__(self) -> str:
        return f"Node<{self.id}, {'{0:.3f}'.format(self.depth)}>"
class ClusterTree:
    nodes: "list[TreeNode]" = []
    def __init__(self, leafCount: int):
        self.leafCount = leafCount
        for i in range(leafCount):
            self.nodes.append(TreeNode(i, [], 0, True))
    def addParent(self, id: int, childrenIds: "list[int]", depth: int) -> TreeNode:
        children = [self.nodes[x] for x in childrenIds]
        node = TreeNode(id, children, depth, False)
        self.nodes.append(node)
        return node
    def getRoots(self) -> "list[TreeNode]":
        return list(filter(lambda x: x.parent == None, self.nodes))
    def freezeTree(self) -> None:
        for node in self.nodes:
            node.cacheAbsoluteChildCount()
    
