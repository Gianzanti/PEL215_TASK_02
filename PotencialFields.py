import numpy as np
import matplotlib.pyplot as plt

# from icecream import ic


class PotencialFields:
    def __init__(
        self,
        size: tuple[int, int],
        goal: tuple[int, int],
        obstacles: list[tuple[int, int, int]],
    ) -> None:
        """
        size [Tamanho da arena]: (X units, Y units)

        goal [Coordenada do objetivo]: (X, Y)

        obstacles [Lista das coordenas dos obstáculos]: [(X, Y, radius), ...]
        """
        self.sizeX, self.sizeY = size
        self.coords = np.zeros(size)
        self.goal = goal
        self.obstacles = obstacles

    def attractivePotencial(self, Katt=1):
        ua = np.zeros_like(self.coords)

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                dist = np.sqrt((self.goal[0] - x) ** 2 + (self.goal[1] - y) ** 2)
                ua[x][y] = 0.5 * Katt * dist**2

        return ua

    def repulsionPotencial(self, Krep=50):
        up = np.zeros_like(self.coords)

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                for obstacle in self.obstacles:
                    dist = np.sqrt((obstacle[0] - x) ** 2 + (obstacle[1] - y) ** 2)
                    if dist == 0:
                        up[x][y] += Krep
                    elif dist <= obstacle[2]:
                        up[x][y] += 0.5 * Krep * (1 / dist - 1 / obstacle[2]) ** 2

        return up

    def calculatePotencialField(self, Katt=1, Krep=50):
        return self.attractivePotencial(Katt) + self.repulsionPotencial(Krep)

    def showPlot(self, u):
        fig, ax = plt.subplots(figsize=(20, 20))
        plt.imshow(u.T)
        ax.invert_yaxis()

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                text = ax.text(
                    x,
                    y,
                    "{:.1f}".format(u[x, y]),
                    ha="center",
                    va="center",
                    color="w",
                )

        plt.show()
