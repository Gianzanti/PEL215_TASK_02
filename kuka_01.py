from MecanumRobot import MecanumRobot
import math


class KukaAPF(MecanumRobot):
    def __init__(self):
        super().__init__()
        self.state = "decideMovement"
        self.path = [
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 6),
            (5, 6),
            (6, 6),
            (7, 6),
            (8, 7),
            (8, 8),
        ]

        self.currentTarget = 1

    def update(self):
        # print(f"steps: {self.steps}")
        # print(f"state: {self.state}")
        match self.state:
            case "checking":
                checkPosX = abs(self.p["x"] - self.target["x"])
                checkPosY = abs(self.p["y"] - self.target["y"])
                # print(f'Position: X:{self.position["x"]}, Y:{self.position["y"]}')
                # print(f'Target: X:{self.target["x"]}, Y:{self.target["y"]}')
                # print(
                #     f"posX: {checkPosX} [{checkPosX < 0.01}] - posY: {checkPosY} [{checkPosY < 0.01}]"
                # )

                if checkPosX < 0.01 and checkPosY < 0.01:
                    self.stop()
                    if (self.currentTarget + 1) < len(self.path):
                        self.currentTarget += 1
                        self.state = self.nextState
                        print(f"Going to next step: {self.path[self.currentTarget]}")
                    else:
                        self.state = "stopped"

            case "decideMovement":
                if self.path[self.currentTarget][0] > math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] == math.ceil(self.p["y"]):
                    self.state = "move_forward_1m"
                elif self.path[self.currentTarget][0] > math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] > math.ceil(self.p["y"]):
                    self.state = "forward_left_1m"
                elif self.path[self.currentTarget][0] == math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] > math.ceil(self.p["y"]):
                    self.state = "move_left_1m"
                elif self.path[self.currentTarget][0] < math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] > math.ceil(self.p["y"]):
                    self.state = "backward_left_1m"
                elif self.path[self.currentTarget][0] < math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] == math.ceil(self.p["y"]):
                    self.state = "move_backward_1m"
                elif self.path[self.currentTarget][0] < math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] < math.ceil(self.p["y"]):
                    self.state = "backward_right_1m"
                elif self.path[self.currentTarget][0] == math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] < math.ceil(self.p["y"]):
                    self.state = "move_right_1m"
                elif self.path[self.currentTarget][0] > math.ceil(
                    self.p["x"]
                ) and self.path[self.currentTarget][1] < math.ceil(self.p["y"]):
                    self.state = "forward_right_1m"
                else:
                    self.state = "stopped"

                print(
                    f'Current Position: {math.ceil(self.p["x"])}, {math.ceil(self.p["y"])}'
                )
                print(f"Next state: {self.state}")

            case "move_forward_1m":
                self.move_forward(self.max_speed)
                self.state = "checking"
                self.target = {"x": self.p["x"] + 1.0, "y": self.p["y"]}
                self.nextState = "decideMovement"
                pass

            case "forward_left_1m":
                self.move_forward_left(self.max_speed)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] + 1.0,
                    "y": self.p["y"] + 1.0,
                }
                self.nextState = "decideMovement"
                pass

            case "move_left_1m":
                self.move_left(self.max_speed)
                self.state = "checking"
                self.target = {"x": self.p["x"], "y": self.p["y"] + 1.0}
                self.nextState = "decideMovement"
                pass

            case "backward_left_1m":
                self.move_backward_left(self.max_speed)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] - 1.0,
                    "y": self.p["y"] + 1.0,
                }
                self.nextState = "decideMovement"
                pass

            case "move_backward_1m":
                self.move_backward(self.max_speed)
                self.state = "checking"
                self.target = {"x": self.p["x"] - 1.0, "y": self.p["y"]}
                self.nextState = "decideMovement"
                pass

            case "backward_right_1m":
                self.move_backward_right(self.max_speed)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] - 1.0,
                    "y": self.p["y"] - 1.0,
                }
                self.nextState = "decideMovement"
                pass

            case "move_right_1m":
                self.move_right(self.max_speed)
                self.state = "checking"
                self.target = {"x": self.p["x"], "y": self.p["y"] - 1.0}
                self.nextState = "decideMovement"
                pass

            case "forward_right_1m":
                self.move_forward_right(self.max_speed)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] + 1.0,
                    "y": self.p["y"] - 1.0,
                }
                self.nextState = "decideMovement"
                pass

            case "stopped":
                pass


if __name__ == "__main__":
    kuka = KukaAPF()
    kuka.run()
