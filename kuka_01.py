import math
from Gradient import gradient_descent_algorithm
from KukaPath import KukaPath
from PotencialFields import PotencialFields
from icecream import ic

if __name__ == "__main__":
    task = 2

    if task == 1:
        start_position = (1, 0)
        path = [
            (1, 0),
            (2, 0),
            (3, 1),
            (3, 2),
            (2, 3),
            (1, 3),
            (0, 2),
            (0, 1),
            (1, 0),
        ]
        kuka = KukaPath(start_position)
        kuka.setPath(path)
        kuka.run()

    elif task == 2:
        start_position = (0, 0)
        kuka = KukaPath(start_position)

        arenaDimensions = (10, 10)
        goal = (8, 8)
        obstacle_radius = 0.305  # m
        robot_radius = kuka.robot_radius  # 0.456 m
        # ic(robot_radius)
        repulsion_radius = math.ceil(obstacle_radius + robot_radius) * 2  # m
        obstacles = [
            (0, 3, repulsion_radius),
            (1, 6, repulsion_radius),
            (2, 0, repulsion_radius),
            (3.5, 1, repulsion_radius),
            (4, 2, repulsion_radius),
            (4, 3, repulsion_radius),
            (4, 5, repulsion_radius),
            (4, 9, repulsion_radius),
            (5, 4, repulsion_radius),
            (6, 2, repulsion_radius),
            (6, 7, repulsion_radius),
        ]
        pf = PotencialFields(arenaDimensions, goal, obstacles)

        Katt = 3
        Krep = 100
        cellsPF = pf.calculatePotencialField(Katt, Krep)
        # ic(cellsPF)
        pf.showPlot(cellsPF)

        shortest_path = gradient_descent_algorithm(cellsPF, start_position)
        # ic(shortest_path)

        kuka.setPath(shortest_path)
        kuka.run()
