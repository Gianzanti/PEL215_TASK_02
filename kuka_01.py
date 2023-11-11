from KukaPath import KukaPath
from PotencialFields import PotencialFields
from icecream import ic


def gradient_descent_algorithm(cellsPF, start_node):
    shortest_path = []
    current_node = ""
    next_node = start_node

    motion = [[1, 0], [0, 1], [-1, 0], [0, -1], [-1, -1], [-1, 1], [1, -1], [1, 1]]

    while next_node != current_node:
        current_node = next_node
        shortest_path.append(current_node)
        cost = cellsPF[current_node[0]][current_node[1]]
        ic(current_node, cost)

        for move in motion:
            neighbor = (current_node[0] + move[0], current_node[1] + move[1])
            if neighbor == current_node:
                continue

            valX = cellsPF[neighbor[0] : neighbor[0] + 1]
            if valX.size == 0:
                continue

            valY = valX[0][neighbor[1] : neighbor[1] + 1]
            if valY.size == 0:
                continue

            # tentative_value = cellsPF[neighbor[0]][neighbor[1]]
            tentative_value = valY[0]
            ic(neighbor, tentative_value)

            if tentative_value < cost:
                cost = tentative_value
                next_node = neighbor
                ic("Lower cost", cost)
    return shortest_path


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
        repulsion_radius = obstacle_radius + robot_radius  # m
        obstacles = [
            (0, 3, repulsion_radius),
            (1, 6, repulsion_radius),
            (2, 0, repulsion_radius),
            (3.5, 1, repulsion_radius),
            (4, 2, repulsion_radius),
            (4, 3, repulsion_radius),
            (4, 5, repulsion_radius),
            (4, 7, repulsion_radius),
            (5, 4, repulsion_radius),
            (6, 2, repulsion_radius),
            (6, 7, repulsion_radius),
        ]
        pf = PotencialFields(arenaDimensions, goal, obstacles)

        Katt = 1
        Krep = 50
        cellsPF = pf.calculatePotencialField(Katt, Krep)
        # ic(cellsPF)
        pf.showPlot(cellsPF)

        shortest_path = gradient_descent_algorithm(cellsPF, start_position)
        ic(shortest_path)

        # path = [
        #     (1, 0),
        #     (2, 0),
        #     (3, 1),
        #     (3, 2),
        #     (2, 3),
        #     (1, 3),
        #     (0, 2),
        #     (0, 1),
        #     (1, 0),
        # ]
        kuka = KukaPath(start_position)
        kuka.setPath(shortest_path)
        kuka.run()
