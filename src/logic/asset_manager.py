from common.interfaces.asset_manager import IAssetManager, IAsset
from common.exceptions import AssetAppendException


class MemoryAssetManager(IAssetManager):

    def __init__(self):
        self.assets = []

    def getAsset(self, assetIndex: int) -> IAsset:
        return self.assets[assetIndex]

    def getAssetCount(self) -> int:
        return len(self.assets)

    def setAsset(self, assetIndex: int, asset: IAsset) -> None:
        if assetIndex < 0:
            raise AssetAppendException(asset, self, assetIndex,
                                       "Asset index must be valid index.")
        elif assetIndex > len(self.assets):
            raise AssetAppendException(asset, self, assetIndex,
                                       "Asset index out of range.")
        elif assetIndex == len(self.assets):
            self.assets.append(asset)
        else:
            self.assets[assetIndex] = asset


class MemoryAsset(IAsset):

    def __init__(self, sequence: str, name: str):
        self.sequence = sequence
        self.name = name