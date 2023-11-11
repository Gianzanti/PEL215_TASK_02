from MecanumRobot import MecanumRobot


class KukaPath(MecanumRobot):
    def __init__(self, pos: tuple[float, float], path: list[tuple[float, float]] = []):
        super().__init__(pos)

        self.state = "checking"
        self.path = path
        self.next = 0
        self.target = {"x": pos[0], "y": pos[1]}

    def setPath(self, path: list[tuple[float, float]]):
        self.path = path

    def move(self):
        self.base_move()

    def odometry(self):
        self.update_position()

    def update(self):
        print(f"steps: {self.steps}")
        print(f"state: {self.state}")
        match self.state:
            case "checking":
                checkPosX = abs(self.p["x"] - self.target["x"])
                checkPosY = abs(self.p["y"] - self.target["y"])
                print(f'Position: X:{self.p["x"]}, Y:{self.p["y"]}')
                print(f'Target: X:{self.target["x"]}, Y:{self.target["y"]}')
                print(
                    f"ΔposX: {checkPosX} [{checkPosX < 0.01}] - ΔposY: {checkPosY} [{checkPosY < 0.01}]"
                )

                if checkPosX < 0.01 and checkPosY < 0.01:
                    self.stop()
                    if (self.next + 1) < len(self.path):
                        self.next += 1
                        self.state = "decideMovement"
                        print(f"Going to next step: {self.path[self.next]}")
                    else:
                        self.state = "stopped"

            case "decideMovement":
                Δx = self.path[self.next][0] - round(self.p["x"], 0)
                Δy = self.path[self.next][1] - round(self.p["y"], 0)
                print(f"Δx: {Δx}, Δy: {Δy}")

                if Δx > 0:
                    if Δy > 0:
                        self.move_forward_left(self.speed_increment)
                    elif Δy == 0:
                        self.move_forward(self.speed_increment)
                    elif Δy < 0:
                        self.move_forward_right(self.speed_increment)
                    else:
                        self.stop()

                elif Δx == 0:
                    if Δy > 0:
                        self.move_left(self.speed_increment)
                    elif Δy == 0:
                        self.stop()
                    elif Δy < 0:
                        self.move_right(self.speed_increment)
                    else:
                        self.stop()

                elif Δx < 0:
                    if Δy > 0:
                        self.move_backward_left(self.speed_increment)
                    elif Δy == 0:
                        self.move_backward(self.speed_increment)
                    elif Δy < 0:
                        self.move_backward_right(self.speed_increment)
                    else:
                        self.stop()

                else:
                    self.stop()

                self.target = {"x": self.p["x"] + Δx, "y": self.p["y"] + Δy}
                self.state = "checking"

                print(
                    f'Current Position: {round(self.p["x"], 0)}, {round(self.p["y"], 0)}'
                )
                print(f"Next state: {self.state}")
