from typing import Callable
from common.interfaces.distance_matrix import IDistanceMatrix
from common.interfaces.distance_calculator import IDistanceCalculator
from common.interfaces.asset_manager import IAssetManager
class API:
    def __init__(self):
        pass


class SplitManager:
    distance_matrix: IDistanceMatrix
    assetManger: IAssetManager
    distanceCalculator: IDistanceCalculator
    def __init__(self, distance_matrix: IDistanceMatrix, assetManger: IAssetManager, distanceCalculator: IDistanceCalculator):
        self.distance_matrix = distance_matrix
        self.assetManger = assetManger
        self.distanceCalculator = distanceCalculator
    
    def calculateDistances(self, statusReport: Callable[[int, int, float], None] = (lambda stepsDone, totalSteps, percetage: None)) -> None:
        self.distanceCalculator.calculateDistances(self.distance_matrix, self.assetManger, statusReport)
    
    def getMatrix(self) -> IDistanceMatrix:
        return self.distance_matrix