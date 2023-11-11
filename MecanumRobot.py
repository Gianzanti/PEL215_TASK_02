from abc import ABC, abstractmethod
from controller import Robot

INF = float("+inf")


class MecanumRobot(ABC):
    def __init__(self, initPos: tuple[float, float] = (0.0, 0.0)) -> None:
        """
        initPos: tuple[float, float] - defines initial position (x,y) for robot, defaults to (0.0, 0.0)
        """
        self.me = Robot()
        self.timestep = int(self.me.getBasicTimeStep()) * 1
        maxVelocity = 14.81 / 2  # rad/s
        self.wheel_radius = 0.05  # m
        self.max_speed = maxVelocity * self.wheel_radius  # m/s
        self.speed_increment = 0.5 * self.max_speed
        self.l = {"x": 0.228, "y": 0.158}  # m
        self.robot_radius = max(self.l["x"], self.l["y"]) * 2  # m
        self.v = {"x": 0.0, "y": 0.0}
        self.p = {"x": initPos[0], "y": initPos[1]}
        self.wheels = []
        self.steps = 0
        self.initMotors()

    def initMotors(self):
        for i in range(0, 4):
            self.wheels.append(self.me.getDevice(f"wheel{i+1}"))

        self.set_wheel_speeds([0, 0, 0, 0])

    def set_wheel_speeds(self, speeds):
        for i in range(0, 4):
            self.wheels[i].setPosition(INF)
            self.wheels[i].setVelocity(speeds[i])

    def base_move(self):
        speeds = [
            1 / self.wheel_radius * (self.v["x"] + self.v["y"]),
            1 / self.wheel_radius * (self.v["x"] - self.v["y"]),
            1 / self.wheel_radius * (self.v["x"] - self.v["y"]),
            1 / self.wheel_radius * (self.v["x"] + self.v["y"]),
        ]
        self.set_wheel_speeds(speeds)
        print(f"Speeds: vx: {self.v['x']:2f}[m/s], vy: {self.v['y']:2f}[m/s]")

    def update_position(self):
        self.p["x"] += self.v["x"] * self.timestep / 1000
        self.p["y"] += self.v["y"] * self.timestep / 1000
        print(f'Position: x: {self.p["x"]:2f}[m], y: {self.p["y"]:2f}[m]')

    def move_forward(self, speed):
        self.v["x"] += speed
        self.v["x"] = self.v["x"] if self.v["x"] < self.max_speed else self.max_speed

    def move_forward_left(self, speed):
        self.v["x"] += speed
        self.v["x"] = self.v["x"] if self.v["x"] < self.max_speed else self.max_speed
        self.v["y"] += speed
        self.v["y"] = self.v["y"] if self.v["y"] < self.max_speed else self.max_speed

    def move_forward_right(self, speed):
        self.v["x"] += speed
        self.v["x"] = self.v["x"] if self.v["x"] < self.max_speed else self.max_speed
        self.v["y"] -= speed
        self.v["y"] = self.v["y"] if self.v["y"] > -self.max_speed else -self.max_speed

    def move_backward(self, speed):
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed

    def move_backward_left(self, speed):
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed
        self.v["y"] += speed
        self.v["y"] = self.v["y"] if self.v["y"] < self.max_speed else self.max_speed

    def move_backward_right(self, speed):
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed
        self.v["y"] -= speed
        self.v["y"] = self.v["y"] if self.v["y"] > -self.max_speed else -self.max_speed

    def stop(self):
        self.v["x"] = 0
        self.v["y"] = 0

    def move_left(self, speed):
        self.v["y"] += speed
        self.v["y"] = self.v["y"] if self.v["y"] < self.max_speed else self.max_speed

    def move_right(self, speed):
        self.v["y"] -= speed
        self.v["y"] = self.v["y"] if self.v["y"] > -self.max_speed else -self.max_speed

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def odometry(self):
        pass

    def run(self):
        while self.me.step(self.timestep) != -1:
            self.update()
            self.move()
            self.odometry()
            self.steps += 1
