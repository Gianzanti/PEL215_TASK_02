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

            tentative_value = valY[0]
            ic(neighbor, tentative_value)

            if tentative_value < cost:
                cost = tentative_value
                next_node = neighbor
                ic("Lower cost", cost)
    return shortest_path
