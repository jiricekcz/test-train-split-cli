import math
from api import API, SplitManager
import time
from argparse import ArgumentParser
from common.types.cli import Args

from logic.asset_manager import MemoryAssetManager
from logic.fasta_asset_loader import FastaAssetLoader
from logic.pairwise_alignment_distance_calculator import PairwiseAlignmentDistanceCalculator
from logic.distance_matrix import NumpyDistanceMatrixDiskBackup
from logic.splitter import RandomSplitter, Split

from util.abs_path import path


class CLI:

    def __init__(self):
        self.api = API()

    def run(self) -> None:
        self.parseArguments()

        assets = MemoryAssetManager()
        loader = FastaAssetLoader(path(__file__, "../data/holo4k.fasta"))
        loader.loadAssets(assets, limit=468)
        assetCount = assets.getAssetCount()
        manager = SplitManager(NumpyDistanceMatrixDiskBackup(assetCount, path(__file__, "../data/out/matrix.npy")), assets,
                               PairwiseAlignmentDistanceCalculator(), RandomSplitter())

        t0 = time.time()
        manager.calculateDistances()
        t1 = time.time()
        print(f"""Calculation time: {'{0:.1f}'.format(t1 - t0)} s""")
        print(manager.getSplits([50, 50]))

    def parseArguments(self) -> None:
        parser = ArgumentParser()
        args: Args = parser.parse_args()
