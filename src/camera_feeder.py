import logging
import threading
import time
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class CameraFeeder:
    CAPTURE_RETRY_MAX: int = 30

    def __init__(self, src: str) -> None:
        self._src: str = src
        self._cap = cv2.VideoCapture(self._src)
        self._frame: Optional[np.ndarray] = None
        self._fail_count: int = 0
        self._cap_thread = threading.Thread(target=self._update)
        self._cap_thread_started: bool = False
        self._read_lock = threading.Lock()

    def _update(self) -> None:
        while self._cap_thread_started:
            ret, frame = self._cap.read()
            with self._read_lock:
                if ret:
                    self._frame = frame
                    self._fail_count = 0
                else:
                    self._frame = None
                    self._fail_count += 1
                    if self._fail_count > CameraFeeder.CAPTURE_RETRY_MAX:
                        logger.warning("VideoCapture retry over, set capture again")
                        self._cap.release()
                        time.sleep(1)
                        self._cap = cv2.VideoCapture(self._src)
                        if self._cap.isOpened is False:
                            logger.error("VideoCapture is not opened")

    def start(self) -> None:
        if self._cap.isOpened:
            self._cap_thread_started = True
            self._cap_thread.start()
        else:
            logger.error("VideoCapture is not opened")

    def read(self) -> Optional[np.ndarray]:
        with self._read_lock:
            if self._frame is None:
                frame = None
            else:
                frame = self._frame.copy()

        return frame

    def stop(self) -> None:
        self._cap_thread.join()
        self._cap_thread_started = False
