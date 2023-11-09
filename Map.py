# from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class Map:
    def __init__(self, size: tuple[int, int]) -> None:
        """size: (X units, Y units)"""
        self.sizeX, self.sizeY = size
        self.coords = np.zeros(size)

    def setGoal(self, goal: tuple[int, int]):
        """goal: (X, Y)"""
        self.goal = goal

    def setObstacles(self, obstacles: list[tuple[int, int, int]]):
        """obstacles: [(X, Y, radius), ...]"""
        self.obstacles = obstacles

    def calculateAttractivePotencial(self, Katt=1):
        self.Ua = np.zeros_like(self.coords)

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                dist = np.sqrt((self.goal[0] - x) ** 2 + (self.goal[1] - y) ** 2)
                self.Ua[x][y] = 0.5 * Katt * dist**2

    def calculateRepulsionPotencial(self, Krep=50):
        self.Up = np.zeros_like(self.coords)

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                for obstacle in self.obstacles:
                    dist = np.sqrt((obstacle[0] - x) ** 2 + (obstacle[1] - y) ** 2)
                    if dist == 0:
                        self.Up[x][y] += Krep
                    elif dist <= obstacle[2]:
                        self.Up[x][y] += 0.5 * Krep * (1 / dist - 1 / obstacle[2]) ** 2

    def calculateTotalPotencial(self):
        self.U = self.Ua + self.Up

        fig, ax = plt.subplots(figsize=(20, 20))
        plt.imshow(self.U)

        for i in range(self.sizeX):
            for j in range(self.sizeY):
                text = ax.text(
                    j,
                    i,
                    "{:.0f}".format(self.U[i, j]),
                    ha="center",
                    va="center",
                    color="w",
                )

        plt.show()

        print(self.U)


if __name__ == "__main__":
    map = Map((20, 20))
    map.setGoal((4, 11))
    map.setObstacles([(5, 5, 20), (5, 6, 20), (6, 6, 20), (2, 2, 10), (10, 7, 5)])
    map.calculateAttractivePotencial(1)
    map.calculateRepulsionPotencial(50)
    map.calculateTotalPotencial()
