import threading
import time
from logging import DEBUG, INFO, basicConfig, getLogger, handlers

import cv2

from camera_feeder import CameraFeeder
from control_tank import ControlTank
from face_detector import FaceDetector

basicConfig(
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    level=INFO,
    handlers=[handlers.SysLogHandler(address="/dev/log")],
)
logger = getLogger(__name__)


class MainSystem:
    CAPTURE_SRC: str = "nvarguscamerasrc sensor_mode=2 ! nvvidconv ! video/x-raw, format=(string)I420 ! videoconvert ! appsink"

    def __init__(self) -> None:
        self._main_thread = threading.Thread(target=self._main)
        self._control_tank = ControlTank()
        self._camera_feeder = CameraFeeder(MainSystem.CAPTURE_SRC)
        self._face_detector = FaceDetector()
        self._counter: int = 0

    def start(self) -> None:
        try:
            self._control_tank.initialize()
            logger.info("control tank initialized")
            self._camera_feeder.start()
            logger.info("camera feeder started")
            time.sleep(3)
            self._main_thread.start()
            logger.info("system started")
        except Exception as ex:
            logger.error(f"system encontered exception on startup: {ex}")

    def stop(self) -> None:
        self._main_thread.join()

    def _main(self) -> None:
        frame = self._camera_feeder.read()
        if frame is not None:
            logger.info(f"frame.shape: {frame.shape}")
            cv2.imwrite("./temp/1st_frame.jpg", frame)
        while frame is not None:
            try:
                faces = self._face_detector.detect(frame)
                if faces == []:
                    pass
                else:
                    self._counter += 1
                    for face in faces:
                        p1 = (face[0], face[1])
                        p2 = (face[0] + face[2], face[1] + face[3])
                        cv2.rectangle(frame, p1, p2, (0, 0, 255), 3)
                    cv2.imwrite(f"./temp/face_{self._counter:05}.jpg", frame)
                    logger.info(f"detect faces: {faces}")

                frame = self._camera_feeder.read()
            except Exception as ex:
                raise (ex)


main_system = MainSystem()
main_system.start()
main_system.stop()
