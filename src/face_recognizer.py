# Face Detector model : https://github.com/sr6033/face-detection-with-OpenCV-and-DNN

import glob
import logging
import os
from enum import Enum
from typing import List, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class FaceLabel(Enum):
    abe_hiroshi = 0
    hirose_suzu = 1
    me = 2


class FaceRecognizer:
    FACE_RECOGNIZER_MODEL_PATH: str = "./assets/model/face_recognizer.yml"
    FACE_IMAGE_SIZE: Tuple[int, int] = (200, 200)
    FACE_DETECTION_CONF_TH: float = 0.3
    FACE_RECOGNITION_CONF_TH: float = 3500.0

    def __init__(self) -> None:
        self._detector = cv2.dnn_DetectionModel(
            "./assets/model/res10_300x300_ssd_iter_140000.caffemodel", "./assets/model/deploy.prototxt"
        )
        self._detector.setInputSize(300, 300)
        self._detector.setInputMean((104.0, 177.0, 123.0))
        # self._recognizer = cv2.face_LBPHFaceRecognizer.create()
        self._recognizer = cv2.face_FisherFaceRecognizer.create()
        if os.path.exists(FaceRecognizer.FACE_RECOGNIZER_MODEL_PATH):
            logger.info("Load Face Recognizer model")
            self._recognizer.read(FaceRecognizer.FACE_RECOGNIZER_MODEL_PATH)
        else:
            # train images and save face recognition model(yaml)
            cropped_images: List[np.ndarray] = []
            labels: List[int] = []
            # image file name format : face_{label}_{num}.jpg
            image_path_list = glob.glob("./assets/images/*.jpg")
            for image_path in image_path_list:
                label = int(image_path.split("_")[1])
                image = cv2.imread(image_path)
                _, _, bboxes = self.detect(image)
                if len(bboxes) == 0:
                    continue
                x = bboxes[0][0]
                y = bboxes[0][1]
                w = bboxes[0][2]
                h = bboxes[0][3]
                cropped_images.append(
                    cv2.resize(
                        cv2.cvtColor(image[y : y + h, x : x + w], cv2.COLOR_BGR2GRAY), FaceRecognizer.FACE_IMAGE_SIZE
                    )
                )
                labels.append(label)

            logger.info("Train Face Recognizer model")
            self._recognizer.train(cropped_images, np.array(labels))
            logger.info("Save Face Recognizer model")
            self._recognizer.write(FaceRecognizer.FACE_RECOGNIZER_MODEL_PATH)

    def detect(self, frame: np.ndarray) -> Tuple[List[int], List[float], List[Tuple[int, int, int, int]]]:
        return self._detector.detect(frame, confThreshold=FaceRecognizer.FACE_DETECTION_CONF_TH)

    def recognize(self, image: np.ndarray) -> Tuple[int, float]:
        return self._recognizer.predict(image)
