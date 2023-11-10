from MecanumRobot import MecanumRobot


class KukaHexagon(MecanumRobot):
    def __init__(self):
        super().__init__()
        self.state = "move_forward_1m"

    def update(self):
        print(f"steps: {self.steps}")
        print(f"state: {self.state}")
        match self.state:
            case "checking":
                checkPosX = abs(self.p["x"] - self.target["x"])
                checkPosY = abs(self.p["y"] - self.target["y"])
                print(
                    f"posX: {checkPosX} [{checkPosX < 0.01}] - posY: {checkPosY} [{checkPosY < 0.01}]"
                )

                if checkPosX < 0.01 and checkPosY < 0.01:
                    self.stop()
                    self.state = self.nextState

            case "move_forward_1m":
                self.move_forward(self.speed_increment * 3)
                self.state = "checking"
                self.target = {"x": self.p["x"] + 1.0, "y": self.p["y"]}
                self.nextState = "forward_left_1m"
                pass

            case "forward_left_1m":
                self.move_forward_left(self.speed_increment * 3)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] + 1.0,
                    "y": self.p["y"] + 1.0,
                }
                self.nextState = "move_left_1m"
                pass

            case "move_left_1m":
                self.move_left(self.speed_increment * 3)
                self.state = "checking"
                self.target = {"x": self.p["x"], "y": self.p["y"] + 1.0}
                self.nextState = "backward_left_1m"
                pass

            case "backward_left_1m":
                self.move_backward_left(self.speed_increment * 3)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] - 1.0,
                    "y": self.p["y"] + 1.0,
                }
                self.nextState = "move_backward_1m"
                pass

            case "move_backward_1m":
                self.move_backward(self.speed_increment * 3)
                self.state = "checking"
                self.target = {"x": self.p["x"] - 1.0, "y": self.p["y"]}
                self.nextState = "backward_right_1m"
                pass

            case "backward_right_1m":
                self.move_backward_right(self.speed_increment * 3)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] - 1.0,
                    "y": self.p["y"] - 1.0,
                }
                self.nextState = "move_right_1m"
                pass

            case "move_right_1m":
                self.move_right(self.speed_increment * 3)
                self.state = "checking"
                self.target = {"x": self.p["x"], "y": self.p["y"] - 1.0}
                self.nextState = "forward_right_1m"
                pass

            case "forward_right_1m":
                self.move_forward_right(self.speed_increment * 3)
                self.state = "checking"
                self.target = {
                    "x": self.p["x"] + 1.0,
                    "y": self.p["y"] - 1.0,
                }
                self.nextState = "move_forward_1m"
                pass

            case "stopped":
                pass


if __name__ == "__main__":
    kuka = KukaHexagon()
    kuka.run()


# (0, 0) -> (1, 1) -> (2, 2) -> (3, 3) -> (4, 4) -> (5, 5) -> (6, 6) -> (7, 7) -> (8, 8) -> (8, 9) -> (8, 10) -> (8, 11)
