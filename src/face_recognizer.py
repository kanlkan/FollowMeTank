import glob
import logging
from typing import List

import cv2
import numpy as np
import scipy

logger = logging.getLogger(__name__)


class FaceDetector:
    def __init__(self) -> None:
        self._detector = cv2.CascadeClassifier("./assets/haarcascade_frontalface_default.xml")

    def detect(self, frame: np.ndarray) -> List[List[int]]:
        boxes = self._detector.detectMultiScale(frame)
        return boxes
