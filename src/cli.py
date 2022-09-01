import math
from api import API, SplitManager
import time
from argparse import ArgumentParser
from common.types.cli import Args

from logic.asset_manager import MemoryAssetManager
from logic.fasta_asset_loader import FastaAssetLoader
from logic.pairwise_alignment_distance_calculator import PairwiseAlignmentDistanceCalculator, PairwiseAlignmentScoreDistanceCalculator
from logic.distance_matrix import NumpyDistanceMatrixDiskBackup
from logic.agglomerative_clustering_splitter import AgglomerativeClusteringSplitter

from util.abs_path import path


class CLI:

    def __init__(self):
        self.api = API()

    def run(self) -> None:
        self.parseArguments()
        limit = 200
        assets = MemoryAssetManager()
        loader = FastaAssetLoader(path(__file__, "../data/holo4k.fasta"))
        loader.loadAssets(assets, limit=limit)
        filenameAddition = "" if limit == None else f"_{limit}x{limit}"
        assetCount = assets.getAssetCount()
        manager = SplitManager(NumpyDistanceMatrixDiskBackup(assetCount, path(__file__, f"../data/out/matrix_BLOSUM62_SCORE{filenameAddition}.npy"), save_loop_length=100_000), assets,
                               PairwiseAlignmentScoreDistanceCalculator(), AgglomerativeClusteringSplitter(headstartFactor=15))

        t0 = time.time()
        manager.calculateDistances()
        t1 = time.time()
        print(f"""Calculation time: {'{0:.1f}'.format(t1 - t0)} s""")
        splits = manager.getSplits([60, 30, 10])
        for split in splits:
            print(split)

    def parseArguments(self) -> None:
        parser = ArgumentParser()
        args: Args = parser.parse_args()
