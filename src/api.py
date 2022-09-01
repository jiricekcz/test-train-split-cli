from typing import Callable, Iterable
from common.interfaces.distance_matrix import IDistanceMatrix
from common.interfaces.distance_calculator import IDistanceCalculator
from common.interfaces.asset_manager import IAssetManager
from common.interfaces.splitter import ISplit, ISplitter


class SplitManager:
    distance_matrix: IDistanceMatrix
    assetManger: IAssetManager
    distanceCalculator: IDistanceCalculator
    splitter: ISplitter

    def __init__(self, distance_matrix: IDistanceMatrix,
                 assetManger: IAssetManager,
                 distanceCalculator: IDistanceCalculator,
                 splitter: ISplitter):
        self.distance_matrix = distance_matrix
        self.assetManger = assetManger
        self.distanceCalculator = distanceCalculator
        self.splitter = splitter

    def calculateDistances(
        self,
        statusReport: Callable[[int, int, float], None] = (
            lambda stepsDone, totalSteps, percetage: None)
    ) -> None:
        self.distanceCalculator.calculateDistances(self.distance_matrix,
                                                   self.assetManger,
                                                   statusReport)

    def getSplits(self, distribution: "list[int]") -> Iterable[ISplit]:
        return self.splitter.calculateSplit(self.distance_matrix, distribution)

    def getMatrix(self) -> IDistanceMatrix:
        return self.distance_matrix