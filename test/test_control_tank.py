import argparse
import sys

sys.path.append("../")
from src.control_tank import ControlTank


class Test_ControlTank:
    def __init__(self) -> None:
        self._control_tank = ControlTank()

    def exec(self, test_no: int) -> None:
        self._control_tank.initialize()
        if test_no == 0:
            self._test_control_tank_0()
        elif test_no == 1:
            self._test_control_tank_1()
        elif test_no == 2:
            self._test_control_tank_2()
        elif test_no == 3:
            self._test_control_tank_3()
        elif test_no == 4:
            self._test_control_tank_4()
        else:
            pass

    def _test_control_tank_0(self) -> None:
        self._control_tank.stop()

    def _test_control_tank_1(self) -> None:
        self._control_tank.move_forward()

    def _test_control_tank_2(self) -> None:
        self._control_tank.move_backward()

    def _test_control_tank_3(self) -> None:
        self._control_tank.turn_clockwise()

    def _test_control_tank_4(self) -> None:
        self._control_tank.turn_counterclockwise()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_no", "-n", type=int)
    args = parser.parse_args()

    test_control_tank = Test_ControlTank()
    test_control_tank.exec(args.test_no)
