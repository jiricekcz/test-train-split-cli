from api import API, SplitManager
from argparse import ArgumentParser
from common.types.cli import Args

from logic.asset_manager import MemoryAssetManager
from logic.pairwise_alignment_distance_calculator import PaiwiseAlignmentDistanceCalculator
from logic.distance_matrix import NumpyDistanceMatrix
class CLI:
    def __init__(self):
        self.api = API()
    def run(self) -> None:
        parser = ArgumentParser()


        args: Args = parser.parse_args()


