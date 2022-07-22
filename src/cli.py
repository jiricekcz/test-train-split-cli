from api import API, SplitManager
from argparse import ArgumentParser
from common.types.cli import Args

from logic.asset_manager import MemoryAssetManager
from logic.fasta_asset_loader import FastaAssetLoader
from logic.pairwise_alignment_distance_calculator import PaiwiseAlignmentDistanceCalculator
from logic.distance_matrix import NumpyDistanceMatrix
from util.abs_path import path


class CLI:

    def __init__(self):
        self.api = API()

    def run(self) -> None:
        self.parseArguments()

        assets = MemoryAssetManager()
        loader = FastaAssetLoader(path(__file__, "../data/holo4k.fasta"))
        loader.loadAssets(assets, limit=10)
        assetCount = assets.getAssetCount()
        manager = SplitManager(NumpyDistanceMatrix(assetCount), assets,
                               PaiwiseAlignmentDistanceCalculator())
        manager.calculateDistances()
        print(manager.distance_matrix.getRawMatrix())

    def parseArguments(self) -> None:
        parser = ArgumentParser()
        args: Args = parser.parse_args()
