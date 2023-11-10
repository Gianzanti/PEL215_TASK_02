from abc import ABC, abstractmethod
from controller import Robot

INF = float("+inf")


class MecanumRobot(ABC):
    def __init__(self) -> None:
        self.me = Robot()
        self.timestep = int(self.me.getBasicTimeStep()) * 1
        maxVelocity = 14.81 / 2  # rad/s
        self.wheel_radius = 0.05  # m
        self.max_speed = maxVelocity * self.wheel_radius  # m/s
        # self.speed_increment = self.max_speed
        self.l = {"x": 0.228, "y": 0.158}
        self.v = {"x": 0.0, "y": 0.0}
        self.p = {"x": 0.0, "y": 0.0}
        self.steps = 0
        self.initMotors()

    def initMotors(self):
        self.wheels = []
        for i in range(0, 4):
            self.wheels.append(self.me.getDevice(f"wheel{i+1}"))

        speeds = [0, 0, 0, 0]
        self.set_wheel_speeds(speeds)

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
        self.base_move()

    def move_forward_left(self, speed):
        self.v["x"] += speed
        self.v["x"] = self.v["x"] if self.v["x"] < self.max_speed else self.max_speed
        self.v["y"] += speed
        self.v["y"] = self.v["y"] if self.v["y"] < self.max_speed else self.max_speed
        self.base_move()

    def move_forward_right(self, speed):
        self.v["x"] += speed
        self.v["x"] = self.v["x"] if self.v["x"] < self.max_speed else self.max_speed
        self.v["y"] -= speed
        self.v["y"] = self.v["y"] if self.v["y"] > -self.max_speed else -self.max_speed
        self.base_move()

    def move_backward(self, speed):
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed
        self.base_move()

    def move_backward_left(self, speed):
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed
        self.v["y"] += speed
        self.v["y"] = self.v["y"] if self.v["y"] < self.max_speed else self.max_speed
        self.base_move()

    def move_backward_right(self, speed):
        self.v["x"] -= speed
        self.v["x"] = self.v["x"] if self.v["x"] > -self.max_speed else -self.max_speed
        self.v["y"] -= speed
        self.v["y"] = self.v["y"] if self.v["y"] > -self.max_speed else -self.max_speed
        self.base_move()

    def stop(self):
        self.v["x"] = 0
        self.v["y"] = 0
        self.v["w"] = 0
        self.base_move()

    def move_left(self, speed):
        self.v["y"] += speed
        self.v["y"] = self.v["y"] if self.v["y"] < self.max_speed else self.max_speed
        self.base_move()

    def move_right(self, speed):
        self.v["y"] -= speed
        self.v["y"] = self.v["y"] if self.v["y"] > -self.max_speed else -self.max_speed
        self.base_move()

    @abstractmethod
    def update(self):
        pass

    def run(self):
        while self.me.step(self.timestep) != -1:
            self.update()
            self.update_position()
            self.steps += 1
