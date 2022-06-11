import numpy
from common.interfaces.distance_matrix import IDistanceMatrix
from typing import Iterable, Tuple
class NumpyDistanceMatrix(IDistanceMatrix):
    size: int
    def __init__(self, size: int):
        self.size = size
        self.matrix = numpy.ndarray(shape=(size, size), dtype=numpy.uint16)
        self.matrix.fill(0)
    def getRawDistance(self, x: int, y: int) -> int:
        return int(self.matrix[x][y])
    def setRawDistance(self, x: int, y: int, value: int) -> None:
        self.matrix[x][y] = value
    def getMinMaxRawDistance(self) -> Tuple[int, int]:
        return 0, numpy.iinfo(numpy.uint16).max
    def getMatrixSize(self) -> int:
        return self.size
    def getRawMatrix(self) -> Iterable[Iterable[int]]:
        return self.matrix.tolist()
