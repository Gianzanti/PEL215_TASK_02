import numpy as np
import matplotlib.pyplot as plt


# creating two evenly spaced array with ranging from
# -10 to 10
x = np.arange(-0, 50, 1)
y = np.arange(-0, 50, 1)

# Creating the meshgrid
X, Y = np.meshgrid(x, y)

# Creating delx and dely array
Δx = np.zeros_like(X)
Δy = np.zeros_like(Y)
s = 7
GOAL_RADIUS = 2

GOAL_X = 33
GOAL_Y = 40
GOAL = (GOAL_X, GOAL_Y)

OBSTACLE_X = 25
OBSTACLE_Y = 25
OBST = (OBSTACLE_X, OBSTACLE_Y)


for i in range(len(x)):
    for j in range(len(y)):
        distance_goal = np.sqrt((GOAL[0] - X[i][j]) ** 2 + (GOAL[1] - Y[i][j]) ** 2)
        distance_obst = np.sqrt((OBST[0] - X[i][j]) ** 2 + (OBST[1] - Y[i][j]) ** 2)

        θ_goal = np.arctan2(GOAL[1] - Y[i][j], GOAL[0] - X[i][j])
        θ_obst = np.arctan2(Y[i][j] - OBST[1], X[i][j] - OBST[0])

        if distance_obst < GOAL_RADIUS:
            Δx[i][j] = np.sign(np.cos(θ_obst))
            Δy[i][j] = np.sign(np.cos(θ_obst))

        elif distance_obst > GOAL_RADIUS + s:
            Δx[i][j] = 0  # + (50 * s * np.cos(θ_obst))
            Δy[i][j] = 0  # + (50 * s * np.sin(θ_obst))

        elif distance_obst <= GOAL_RADIUS + s:
            Δx[i][j] = 50 + (s + GOAL_RADIUS - distance_obst) * np.cos(θ_obst)
            Δy[i][j] = 50 + (s + GOAL_RADIUS - distance_obst) * np.sin(θ_obst)

        # if distance_goal < GOAL_RADIUS + s:
        #     if Δx[i][j] != 0:
        #         Δx[i][j] += 50 * (distance_goal - GOAL_RADIUS) * np.cos(θ_goal)
        #         Δy[i][j] += 50 * (distance_goal - GOAL_RADIUS) * np.sin(θ_goal)
        #     else:
        #         Δx[i][j] = 50 * (distance_goal - GOAL_RADIUS) * np.cos(θ_goal)
        #         Δy[i][j] = 50 * (distance_goal - GOAL_RADIUS) * np.sin(θ_goal)

        # if distance_goal >= GOAL_RADIUS + s:
        #     if Δx[i][j] != 0:
        #         Δx[i][j] += 50 * s * np.cos(θ_goal)
        #         Δy[i][j] += 50 * s * np.sin(θ_goal)
        #     else:
        #         Δx[i][j] = 50 * s * np.cos(θ_goal)
        #         Δy[i][j] = 50 * s * np.sin(θ_goal)


print(Δx)
print(Δy)

fig, ax = plt.subplots(figsize=(10, 10))
ax.quiver(X, Y, Δx, Δy)

ax.add_patch(plt.Circle((GOAL[0], GOAL[1]), GOAL_RADIUS, color="y"))
ax.add_patch(plt.Circle((OBST[0], OBST[1]), GOAL_RADIUS, color="m"))

ax.annotate("Goal", xy=(GOAL[0], GOAL[1] - 0.25), fontsize=10, ha="center")
ax.annotate("Obstacle", xy=(OBST[0], OBST[1] - 0.25), fontsize=8, ha="center")

ax.set_title("Combined Potential when Goal and Obstacle are different")

plt.show()
