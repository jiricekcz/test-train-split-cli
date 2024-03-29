import os
import numpy
from common.interfaces.distance_matrix import IDistanceMatrix
from typing import Iterable, Tuple



class NumpyDistanceMatrix(IDistanceMatrix):
    """
    Saves the disctances to a matrix in memory.
    """
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

    def getNumpyNDArray(self) -> numpy.ndarray:
        return self.matrix


class NumpyDistanceMatrixDiskBackup(IDistanceMatrix):
    """
    Saves the disctances to a matrix in memory. This matrix is also saved to a file in specified intervals.
    """
    size: int
    matrix: numpy.ndarray
    file_name: str
    save_on_edit: bool
    edits: int = 0
    save_loop_length: int

    def __init__(self,
                 size: int,
                 file_name: str,
                 save_on_edit: bool = True,
                 load_on_init: bool = True,
                 save_loop_length: int = 10000):
        self.size = size
        self.file_name = file_name
        self.matrix = numpy.ndarray(shape=(size, size), dtype=numpy.uint16)
        self.matrix.fill(0)
        self.save_on_edit = save_on_edit
        self.save_loop_length = save_loop_length
        if load_on_init:
            self.load()
            all = self.matrix.size
            filled = len(self.matrix.nonzero()[0])
            print(
                f"Loaded matrix with {filled}/{all} filled cells, that is {'{0:.2f}'.format(filled / all * 100)}%"
            )

    def filledFraction(self) -> float:
        return len(self.matrix.nonzero()[0]) / self.matrix.size

    def getRawDistance(self, x: int, y: int) -> int:
        return int(self.matrix[x][y])

    def setRawDistance(self, x: int, y: int, value: int) -> None:
        self.matrix[x][y] = value
        self.edits += 1
        if self.save_on_edit and self.edits % self.save_loop_length == 0:
            self.save()

    def getMinMaxRawDistance(self) -> Tuple[int, int]:
        return 0, numpy.iinfo(numpy.uint16).max

    def getMatrixSize(self) -> int:
        return self.size

    def getRawMatrix(self) -> Iterable[Iterable[int]]:
        return self.matrix.tolist()

    def save(self) -> None:
        """
        Saves the matrix to a file.
        """
        dir = os.path.dirname(self.file_name)
        os.makedirs(dir, exist_ok=True)
        print(f"Saving matrix...\r", end="")
        self.matrix.tofile(self.file_name)
        print(
            f"Matrix saved, filled from {'{0:.2f}'.format(self.filledFraction() * 100)}%"
            .ljust(30))

    def load(self) -> None:
        if not os.path.exists(self.file_name): return
        self.matrix = numpy.fromfile(self.file_name, dtype=numpy.uint16)
        self.matrix = self.matrix.reshape(self.size, self.size)

    def getNumpyNDArray(self) -> numpy.ndarray:
        return self.matrix

    def __del__(self):
        self.save()