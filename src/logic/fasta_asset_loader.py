from common.interfaces.asset_loader import IAssetLoader
from common.interfaces.asset_manager import IAssetManager
from Bio import SeqIO

from logic.asset_manager import MemoryAsset


class FastaAssetLoader(IAssetLoader):
    filepath: str

    def __init__(self, filepath: str):
        self.filepath = filepath

    def loadAssets(self, assetManager: IAssetManager, limit: int=None) -> None:
        records = SeqIO.parse(self.filepath, "fasta")
        i = 0
        for r in records:
            if limit is not None and i >= limit:
                break
            assetManager.setAsset(i, MemoryAsset(r.seq, r.id))
            i += 1