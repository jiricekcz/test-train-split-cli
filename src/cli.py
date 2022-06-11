from api import API, SplitManager
from argparse import ArgumentParser
from common.types.cli import Args

from logic.asset_manager import MemoryAssetManager
from logic.distance_calculator import RandomDistanceCalculator
from logic.distance_matrix import NumpyDistanceMatrix
class CLI:
    def __init__(self):
        self.api = API()
    def run() -> None:
        parser = ArgumentParser()


        args: Args = parser.parse_args()

        assetManager = MemoryAssetManager()
        distanceCalculator = RandomDistanceCalculator()
        distanceMatrix = NumpyDistanceMatrix(5)

        m = SplitManager(distanceMatrix, assetManager, distanceCalculator)
        print(m.getMatrix().getRawMatrix())


