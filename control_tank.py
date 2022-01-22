import os
import subprocess
import threading
import time
import logging

logger = logging.getLogger(__name__)


class ControlTank():
    PWM_DUTY_A: float = 0.5
    PWM_DUTY_B: float = 0.5

    def __init__(self) -> None:
        self._enable_a: bool = False
        self._enable_b: bool = False
        self._pwm_thread_a = threading.Thread(target=self._pwm_a_loop)
        self._pwm_thread_b = threading.Thread(target=self._pwm_b_loop)

    def initialize(self) -> bool:
        ret = self._setup_gpio()
        if ret is False:
            return False

        self._start_pwm_threads()
        return True

    def _setup_gpio(self) -> bool:
        # Map GPIO12, GPIO13, GPIO14, GPIO15 (pin 37, 22, 13, 18)
        with open('/sys/class/gpio/export', 'w') as dev_file:
            if os.path.exists('/sys/class/gpio/gpio12') is False:
                ret = subprocess.run(['echo', '12'], stdout=dev_file)
                if ret.returncode != 0:
                    return False
            if os.path.exists('/sys/class/gpio/gpio13') is False:
                ret = subprocess.run(['echo', '13'], stdout=dev_file)
                if ret.returncode != 0:
                    return False
            if os.path.exists('/sys/class/gpio/gpio14') is False:
                ret = subprocess.run(['echo', '14'], stdout=dev_file)
                if ret.returncode != 0:
                    return False
            if os.path.exists('/sys/class/gpio/gpio15') is False:
                ret = subprocess.run(['echo', '15'], stdout=dev_file)
                if ret.returncode != 0:
                    return False

        # Wait for mapping GPIO
        time.sleep(3)

        # Set direction as out on GPIO12 (pin 37)
        with open('/sys/class/gpio/gpio12/direction', 'w') as dev_file:
            ret = subprocess.run(['echo', 'out'], stdout=dev_file)
            if ret.returncode != 0:
                return False

        # Set direction as out on GPIO13 (pin 22)
        with open('/sys/class/gpio/gpio13/direction', 'w') as dev_file:
            ret = subprocess.run(['echo', 'out'], stdout=dev_file)
            if ret.returncode != 0:
                return False

        # Set direction as out on GPIO14 (pin 13)
        with open('/sys/class/gpio/gpio14/direction', 'w') as dev_file:
            ret = subprocess.run(['echo', 'out'], stdout=dev_file)
            if ret.returncode != 0:
                return False

        # Set direction as out on GPIO15 (pin 18)
        with open('/sys/class/gpio/gpio15/direction', 'w') as dev_file:
            ret = subprocess.run(['echo', 'out'], stdout=dev_file)
            if ret.returncode != 0:
                return False

        return True

    def _set_gpio(self, addr: int, value: int) -> bool:
        with open(f'/sys/class/gpio/gpio{addr}/value', 'w') as dev_file:
            ret = subprocess.run(['echo', f'{value}'], stdout=dev_file)
            if ret.returncode != 0:
                return False
        return True

    def _start_pwm_threads(self) -> None:
        self._pwm_thread_a.start()
        self._pwm_thread_b.start()

    def _pwm_a_loop(self) -> None:
        while True:
            if self._enable_a is True:
                self._set_gpio(12, 1)
                time.sleep(ControlTank.PWM_DUTY_A / 10)
                self._set_gpio(12, 0)
                time.sleep(0.1 - ControlTank.PWM_DUTY_A / 10)
            else:
                self._set_gpio(12, 0)

    def _pwm_b_loop(self) -> None:
        while True:
            if self._enable_b is True:
                self._set_gpio(14, 1)
                time.sleep(ControlTank.PWM_DUTY_B / 10)
                self._set_gpio(14, 0)
                time.sleep(0.1 - ControlTank.PWM_DUTY_B / 10)
            else:
                self._set_gpio(14, 0)

    def _set_moter_direction_a(self, value: int):
        return self._set_gpio(13, value)

    def _set_moter_direction_b(self, value: int):
        return self._set_gpio(15, value)

    def move_forward(self) -> None:
        ret = self._set_moter_direction_a(0)
        if ret is False:
            logger.error('failed to move_forward')
            return
        ret = self._set_moter_direction_b(0)
        if ret is False:
            logger.error('failed to move_forward')
            return

        self._enable_a = True
        self._enable_b = True

    def move_backward(self) -> None:
        ret = self._set_moter_direction_a(1)
        if ret is False:
            logger.error('failed to move_backward')
            return
        ret = self._set_moter_direction_b(1)
        if ret is False:
            logger.error('failed to move_backward')
            return

        self._enable_a = True
        self._enable_b = True

    def turn_clockwise(self) -> None:
        ret = self._set_moter_direction_a(1)
        if ret is False:
            logger.error('failed to turn_clockwise')
            return
        ret = self._set_moter_direction_b(0)
        if ret is False:
            logger.error('failed to turn_clockwise')
            return

        self._enable_a = True
        self._enable_b = True

    def turn_counterclockwise(self) -> None:
        ret = self._set_moter_direction_a(0)
        if ret is False:
            logger.error('failed to turn_counterclockwise')
            return
        ret = self._set_moter_direction_b(1)
        if ret is False:
            logger.error('failed to turn_counterclockwise')
            return

        self._enable_a = True
        self._enable_b = True

    def stop(self) -> None:
        self._enable_a = False
        self._enable_b = False

    def finalize(self) -> None:
        self._pwm_thread_a.join()
        self._pwm_thread_b.join()
