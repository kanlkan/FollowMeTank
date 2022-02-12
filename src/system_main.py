import logging
import random
import signal
import sys
import threading
import time
from logging import basicConfig, getLogger, handlers

import cv2

from camera_feeder import CameraFeeder
from control_tank import ControlTank
from face_recognizer import FaceLabel, FaceRecognizer

basicConfig(
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[handlers.SysLogHandler(address="/dev/log")],
)
logger = getLogger(__name__)


class MainSystem:
    CAPTURE_SRC: str = (
        "nvarguscamerasrc sensor_mode=2 ! nvvidconv ! video/x-raw, " "format=(string)I420 ! videoconvert ! appsink"
    )
    ALLOW_NO_FACES: int = 2
    DIFF_MAX_AS_CENTER: int = 200
    FACE_AREA_MAX: int = 25000
    DEBUG_ON: bool = False

    def __init__(self) -> None:
        self._main_thread = threading.Thread(target=self._main)
        self._main_thread_started: bool = False
        self._control_tank = ControlTank()
        self._face_recognier = FaceRecognizer()
        self._camera_feeder = CameraFeeder(MainSystem.CAPTURE_SRC)
        self._follow_me_mode = False
        self._no_face_counter = 0

    def start(self) -> None:
        try:
            self._control_tank.initialize()
            logger.info("control tank initialized")
            self._camera_feeder.start()
            logger.info("camera feeder started")
            time.sleep(3)
            self._main_thread_started = True
            self._main_thread.start()
            signal.signal(signal.SIGTERM, self._signal_handler)
            signal.signal(signal.SIGINT, self._signal_handler)
            logger.info("system started")
        except Exception as ex:
            logger.error(f"system encontered exception on startup: {ex}")

    def stop(self) -> None:
        self._camera_feeder.stop()
        self._main_thread_started = False
        self._main_thread.join()

    def _signal_handler(self, signum, stack) -> None:
        logger.info(f"SIGNAL {signum} recieved")
        self.stop()
        sys.exit(1)

    def _rotate(self, times: int):
        if random.choice((True, False)):
            self._control_tank.turn_clockwise()
        else:
            self._control_tank.turn_counterclockwise()
        time.sleep(2.5 * times)
        self._control_tank.stop()
        time.sleep(0.05)

    def _search_faces(self) -> None:
        # rotate clockwise little by little
        logger.debug("search faces!")
        self._control_tank.turn_clockwise()
        time.sleep(0.05)
        self._control_tank.stop()
        time.sleep(0.05)

    def _follow_me(self, diff: float, face_area: float) -> None:
        logger.debug("Follow me!")
        if face_area > MainSystem.FACE_AREA_MAX:
            logger.debug("arrived")
            self._rotate(1)
            self._follow_me_mode = False
            return

        self._follow_me_mode = True
        if abs(diff) < MainSystem.DIFF_MAX_AS_CENTER:
            # Move forward for zooming target face
            logger.debug("move_forward")
            self._control_tank.move_forward()
            time.sleep(2)
        elif diff < 0:
            logger.debug("turn_clockwise")
            self._control_tank.turn_clockwise()
            time.sleep(0.005)
        else:
            logger.debug("turn_counterclockwise")
            self._control_tank.turn_counterclockwise()
            time.sleep(0.005)
        
        self._control_tank.stop()
        time.sleep(0.05)

    def _main(self) -> None:
        frame = self._camera_feeder.read()
        if frame is not None:
            frame_height, frame_width, _ = frame.shape
            logger.info(f"frame.shape: {frame.shape}")
            self._rotate(1)

        img_counter = 0
        while frame is not None and self._main_thread_started is True:
            try:
                _, _, faces = self._face_recognier.detect(frame)
                if len(faces) == 0:
                    logger.debug("no faces")
                    if self._no_face_counter < MainSystem.ALLOW_NO_FACES:
                        self._no_face_counter += 1
                    else:
                        self._no_face_counter = 0
                        self._follow_me_mode = False
                        self._search_faces()
                else:
                    logger.debug(f"detected faces: {faces}")
                    for face in faces:
                        x, y, w, h = face
                        center = ((x + x + w) / 2, (y + y + h) / 2)
                        face_area = w * h
                        if MainSystem.DEBUG_ON:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            logger.debug(f"save test{img_counter:04}.png")
                            cv2.imwrite(f"./temp/test{img_counter:04}.png", frame)
                        img_counter += 1
                        label, conf = self._face_recognier.recognize(
                            cv2.resize(
                                cv2.cvtColor(frame[y : y + h, x : x + w], cv2.COLOR_RGB2GRAY),
                                FaceRecognizer.FACE_IMAGE_SIZE,
                            )
                        )
                        logger.debug(f"reognized face: {label}, {conf}")
                        if (
                            label == FaceLabel.me.value and conf < FaceRecognizer.FACE_RECOGNITION_CONF_TH
                        ) or self._follow_me_mode is True:
                            diff = frame_width / 2 - center[0]
                            logger.debug(f"diff: {diff}")
                            self._follow_me(diff, face_area)
                        else:
                            self._search_faces()

                frame = self._camera_feeder.read()
            except Exception as ex:
                raise (ex)


main_system = MainSystem()
main_system.start()
