from typing import Callable
from common.interfaces.asset_manager import IAssetManager, IAsset
from common.interfaces.distance_calculator import IDistanceCalculator
from common.interfaces.distance_matrix import IDistanceMatrix
from Bio.Align import PairwiseAligner, substitution_matrices
import numpy as np
class PairwiseAlignmentDistanceCalculator(IDistanceCalculator):
    aligner: PairwiseAligner

    def __init__(self):
        self.aligner: PairwiseAligner = PairwiseAligner()
        self.aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")

    def calculateDistances(
            self,
            distances: IDistanceMatrix,
            assets: IAssetManager,
            statusReport: Callable[[int, int, float], None] = ...) -> None:
        total = distances.getMatrixSize()**2
        for t, x, y, set in distances.elementsToFill():
            set(self.calculateDistance(assets.getAsset(x), assets.getAsset(y)))
            statusReport(t, total, float(t) / float(total))

    def calculateDistance(self, asset1: IAsset, asset2: IAsset) -> float:
        alignments = self.aligner.align(asset1.sequence, asset2.sequence)
        min_size = min(len(asset1.sequence), len(asset2.sequence))
        distance = np.sum(np.diagonal(alignments[0].substitutions)) / min_size
        return distance


# Does not work because scores seem to not work in negative. Negative scores are substituted with 0.
# class PairwiseAlignmentScoreDistanceCalculator(IDistanceCalculator):
#     aligner: PairwiseAligner

#     def __init__(self):
#         self.aligner: PairwiseAligner = PairwiseAligner()
#         self.aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")

#     def calculateDistances(
#             self,
#             distances: IDistanceMatrix,
#             assets: IAssetManager,
#             statusReport: Callable[[int, int, float], None] = ...) -> None:
#         total = distances.getMatrixSize()**2
#         for t, x, y, set in distances.elementsToFill():
#             set(self.calculateDistance(assets.getAsset(x), assets.getAsset(y)))
#             statusReport(t, total, float(t) / float(total))

#     def calculateDistance(self, asset1: IAsset, asset2: IAsset) -> float:
#         score = self.aligner.score(asset1.sequence, asset2.sequence)
#         min_size = min(len(asset1.sequence), len(asset2.sequence))
#         print(self.aligner.score("ME", "LC"))
#         return score / min_size
        