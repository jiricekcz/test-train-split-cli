from random import random
from typing import Callable
from common.interfaces.asset_manager import IAssetManager
from common.interfaces.distance_calculator import IDistanceCalculator
from colorama import Fore, Style
from common.interfaces.distance_matrix import IDistanceMatrix


class RandomDistanceCalculator(IDistanceCalculator):

    def __init__(self):
        print(
            f"{Fore.YELLOW}WARINIG{Style.RESET_ALL}: A random distance calculator is being used! This should never happen unless you are testing the program!"
        )

    def calculateDistances(
            self,
            distances: IDistanceMatrix,
            assets: IAssetManager,
            statusReport: Callable[[int, int, float], None] = ...) -> None:
        size = distances.getMatrixSize()
        for i in range(size):
            for j in range(size):
                distances.setDistance(i, j, random())
                statusReport(i * size + j + 1, size**2,
                             (i * size + j + 1) / (size**2))
