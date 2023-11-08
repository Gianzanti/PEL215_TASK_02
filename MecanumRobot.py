from abc import ABC, abstractmethod
from controller import Robot

INF = float("+inf")


class MecanumRobot(ABC):
    def __init__(self) -> None:
        self.me = Robot()
        self.timestep = int(self.me.getBasicTimeStep()) * 1
        self.max_speed = 0.30  # 6.4  # => 0.7 m/s
        self.speed_increment = 0.05
        self.wheel_radius = 0.05
        self.lenght = {"x": 0.228, "y": 0.158}
        self.velocity = {"x": 0.0, "y": 0.0, "w": 0.0}
        self.position = {"x": 0.0, "y": -2.0, "w": 0.0}
        self.wheelsToMove = [0, 0, 0, 0]
        self.steps = 0

        # self.regular_speed = 6  # => 0.5 m/s
        # self.speed_factor = 0.5
        # self.default_speed = self.speed_factor * self.regular_speed

        # self.r_Distance = 1.0

        # Ku = 0.11
        # # 4210 - 3650 = 560
        # Tu = 560 * self.timestep / 1000

        # # self.Kp = 0.15
        # self.Kp = 0.60 * Ku
        # self.Ki = 2 * self.Kp / Tu
        # self.Kd = self.Kp * Tu / 8

        # # self.Kp = 0.12
        # # self.Ki = 0.0
        # # self.Kd = 0.0

        # print(f"Kp: {self.Kp}")
        # print(f"Ki: {self.Ki}")
        # print(f"Kd: {self.Kd}")

        # self.control_rightDistance = PID(
        #     Kp=self.Kp,
        #     Ki=self.Ki,
        #     Kd=self.Kd,
        #     outMax=self.speed_factor,
        #     outMin=-self.speed_factor,
        #     lim_int_min=-self.max_speed,
        #     lim_int_max=self.max_speed,
        #     T=self.timestep / 1000,
        #     τ=1 / (10 * self.timestep / 1000),
        # )

        self.initMotors()
        # self.initSensors()

    def initMotors(self):
        self.wheels = []
        for i in range(0, 4):
            self.wheels.append(self.me.getDevice(f"wheel{i+1}"))

        self.speeds = [0, 0, 0, 0]
        self.set_wheel_speeds(self.speeds)

    def set_wheel_speeds(self, speeds):
        for i in range(0, 4):
            self.wheels[i].setPosition(INF)
            self.wheels[i].setVelocity(speeds[i])

    def base_move(self):
        self.speeds = [
            1
            / self.wheel_radius
            * (
                self.velocity["x"]
                + self.velocity["y"]
                + self.velocity["w"] * (self.lenght["x"] + self.lenght["y"])
            ),
            1
            / self.wheel_radius
            * (
                self.velocity["x"]
                - self.velocity["y"]
                - self.velocity["w"] * (self.lenght["x"] + self.lenght["y"])
            ),
            1
            / self.wheel_radius
            * (
                self.velocity["x"]
                - self.velocity["y"]
                + self.velocity["w"] * (self.lenght["x"] + self.lenght["y"])
            ),
            1
            / self.wheel_radius
            * (
                self.velocity["x"]
                + self.velocity["y"]
                - self.velocity["w"] * (self.lenght["x"] + self.lenght["y"])
            ),
        ]
        print(f"Speeds: {self.speeds}")
        self.set_wheel_speeds(self.speeds)
        print(
            f"Speeds: vx: {self.velocity['x']:2f}[m/s], vy: {self.velocity['y']:2f}[m/s], ω: {self.velocity['w']:2f}[rad/s]"
        )

    def update_position(self):
        self.position["x"] += self.velocity["x"] * self.timestep / 1000
        self.position["y"] += self.velocity["y"] * self.timestep / 1000
        self.position["w"] += self.velocity["w"] * self.timestep / 1000
        print(
            f'Position: x: {self.position["x"]:2f}[m], y: {self.position["y"]:2f}[m], ω: {self.position["w"]:2f}[rad]'
        )

    def move_forward(self, speed):
        self.velocity["x"] += speed
        self.velocity["x"] = (
            self.velocity["x"]
            if self.velocity["x"] < self.max_speed
            else self.max_speed
        )
        self.base_move()

    def move_forward_left(self, speed):
        self.velocity["x"] += speed
        self.velocity["x"] = (
            self.velocity["x"]
            if self.velocity["x"] < self.max_speed
            else self.max_speed
        )
        self.velocity["y"] += speed
        self.velocity["y"] = (
            self.velocity["y"]
            if self.velocity["y"] < self.max_speed
            else self.max_speed
        )
        self.base_move()

    def move_forward_right(self, speed):
        self.velocity["x"] += speed
        self.velocity["x"] = (
            self.velocity["x"]
            if self.velocity["x"] < self.max_speed
            else self.max_speed
        )
        self.velocity["y"] -= speed
        self.velocity["y"] = (
            self.velocity["y"]
            if self.velocity["y"] > -self.max_speed
            else -self.max_speed
        )
        self.base_move()

    def move_backward(self, speed):
        self.velocity["x"] -= speed
        self.velocity["x"] = (
            self.velocity["x"]
            if self.velocity["x"] > -self.max_speed
            else -self.max_speed
        )
        self.base_move()

    def move_backward_left(self, speed):
        self.velocity["x"] -= speed
        self.velocity["x"] = (
            self.velocity["x"]
            if self.velocity["x"] > -self.max_speed
            else -self.max_speed
        )
        self.velocity["y"] += speed
        self.velocity["y"] = (
            self.velocity["y"]
            if self.velocity["y"] < self.max_speed
            else self.max_speed
        )
        self.base_move()

    def move_backward_right(self, speed):
        self.velocity["x"] -= speed
        self.velocity["x"] = (
            self.velocity["x"]
            if self.velocity["x"] > -self.max_speed
            else -self.max_speed
        )
        self.velocity["y"] -= speed
        self.velocity["y"] = (
            self.velocity["y"]
            if self.velocity["y"] > -self.max_speed
            else -self.max_speed
        )
        self.base_move()

    def stop(self):
        self.velocity["x"] = 0
        self.velocity["y"] = 0
        self.velocity["w"] = 0
        self.base_move()

    def move_left(self, speed):
        self.velocity["y"] += speed
        self.velocity["y"] = (
            self.velocity["y"]
            if self.velocity["y"] < self.max_speed
            else self.max_speed
        )
        self.base_move()

    def move_right(self, speed):
        self.velocity["y"] -= speed
        self.velocity["y"] = (
            self.velocity["y"]
            if self.velocity["y"] > -self.max_speed
            else -self.max_speed
        )
        self.base_move()

    @abstractmethod
    def update(self):
        pass

    # @abstractmethod
    # def move(self):
    #     pass

    def run(self):
        while self.me.step(self.timestep) != -1:
            self.update()
            # self.move()
            self.update_position()
            self.steps += 1
