import numpy as np
import matplotlib.pyplot as plt
from icecream import ic

from Graph import Graph, dijkstra_algorithm, gradient_descent_algorithm, print_result


class Arena:
    def __init__(self, size: tuple[int, int]) -> None:
        """size: (X units, Y units)"""
        self.sizeX, self.sizeY = size
        self.coords = np.zeros(size)
        self.goal = (0, 0)
        self.obstacles = []

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

        # print(self.Up)

    def calculateTotalPotencial(self):
        self.U = self.Ua + self.Up

        fig, ax = plt.subplots(figsize=(20, 20))
        plt.imshow(self.U.T)
        ax.invert_yaxis()

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                text = ax.text(
                    x,
                    y,
                    "{:.1f}".format(self.U[x, y]),
                    ha="center",
                    va="center",
                    color="w",
                )

        return self.U


if __name__ == "__main__":
    goal = (8, 8)
    start = (0, 0)
    xDim = 10
    yDim = 10
    arena = Arena((xDim, yDim))
    arena.setGoal(goal)
    arena.setObstacles(
        [
            (0, 3, 3),
            (1, 6, 3),
            (2, 0, 3),
            (3.5, 1, 3),
            (4, 2, 3),
            (4, 3, 3),
            (4, 5, 3),
            (4, 7, 3),
            (5, 4, 3),
            (6, 2, 3),
            (6, 7, 3),
        ]
    )
    arena.calculateAttractivePotencial(10)
    arena.calculateRepulsionPotencial(100)
    apf = arena.calculateTotalPotencial()

    nodes = [f"({x}, {y})" for x in range(xDim) for y in range(yDim)]

    init_graph: dict[str, dict[str, float]] = {}
    for node in nodes:
        init_graph[node] = {}
        nodeName = node[1:-1]
        coord = tuple(map(int, nodeName.split(", ")))

        N = (coord[0] + 1, coord[1])
        S = (coord[0] - 1, coord[1])
        E = (coord[0], coord[1] + 1)
        W = (coord[0], coord[1] - 1)

        NE = (coord[0] + 1, coord[1] + 1)
        NW = (coord[0] + 1, coord[1] - 1)
        SE = (coord[0] - 1, coord[1] + 1)
        SW = (coord[0] - 1, coord[1] - 1)

        init_graph[node][node] = apf[coord[0]][coord[1]]

        if (N[0] >= 0 and N[1] >= 0) and (N[0] < xDim and N[1] < yDim):
            init_graph[node][f"({N[0]}, {N[1]})"] = apf[N[0]][N[1]]

        if (S[0] >= 0 and S[1] >= 0) and (S[0] < xDim and S[1] < yDim):
            init_graph[node][f"({S[0]}, {S[1]})"] = apf[S[0]][S[1]]

        if (E[0] >= 0 and E[1] >= 0) and (E[0] < xDim and E[1] < yDim):
            init_graph[node][f"({E[0]}, {E[1]})"] = apf[E[0]][E[1]]

        if (W[0] >= 0 and W[1] >= 0) and (W[0] < xDim and W[1] < yDim):
            init_graph[node][f"({W[0]}, {W[1]})"] = apf[W[0]][W[1]]

        if (NE[0] >= 0 and NE[1] >= 0) and (NE[0] < xDim and NE[1] < yDim):
            init_graph[node][f"({NE[0]}, {NE[1]})"] = apf[NE[0]][NE[1]]

        if (NW[0] >= 0 and NW[1] >= 0) and (NW[0] < xDim and NW[1] < yDim):
            init_graph[node][f"({NW[0]}, {NW[1]})"] = apf[NW[0]][NW[1]]

        if (SE[0] >= 0 and SE[1] >= 0) and (SE[0] < xDim and SE[1] < yDim):
            init_graph[node][f"({SE[0]}, {SE[1]})"] = apf[SE[0]][SE[1]]

        if (SW[0] >= 0 and SW[1] >= 0) and (SW[0] < xDim and SW[1] < yDim):
            init_graph[node][f"({SW[0]}, {SW[1]})"] = apf[SW[0]][SW[1]]

    ic(init_graph)
    graph = Graph(nodes, init_graph)

    shortest_path = gradient_descent_algorithm(graph=graph, start_node=f"{start}")
    ic(shortest_path)

    plt.show()
