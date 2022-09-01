from random import random
from typing import Iterable
from common.interfaces.distance_matrix import IDistanceMatrix
from common.interfaces.splitter import ISplitter, ISplit


class Split(ISplit):
    def __init__(self, splits: Iterable[Iterable[int]]):
        self.splits_storage = splits

    def splits(self) -> Iterable[Iterable[int]]:
        return self.splits_storage

    def __str__(self):
        return str("\n".join(map(lambda x: f"[{', '.join(map(str, x))}]", self.splits())))

class RandomSplitter(ISplitter):
    """
    !!!DO NOT USE THIS, THIS IS ONLY A TESTING TOOL!!!*
    """
    def calculateSplit(self, distances: IDistanceMatrix, distribution: "list[int]") -> ISplit:
        lenght = distances.getMatrixSize()
        rv = []
        for i in range(len(distribution)):
            rv.append([])
        for i in range(lenght):
            ind = self.randIndex(distribution)
            rv[ind].append(i)
        
        return Split(rv)
    
    def randIndex(self, distribution: "list[int]") -> int:
        s = sum(distribution)
        r = random() * s
        for i in range(len(distribution)):
            r -= distribution[i]
            if r <= 0:
                return i
