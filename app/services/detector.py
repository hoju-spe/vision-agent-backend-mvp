from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from app.core.config import get_settings


@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox_x1: float
    bbox_y1: float
    bbox_x2: float
    bbox_y2: float


@dataclass
class DetectionResult:
    model_name: str
    inference_ms: float
    result_image_path: Path
    detections: list[Detection]


class YoloDetector:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from ultralytics import YOLO

            self._model = YOLO(self.settings.yolo_model_name)
        return self._model

    def analyze(self, image_path: Path) -> DetectionResult:
        started_at = perf_counter()
        results = self.model.predict(
            source=str(image_path),
            conf=self.settings.confidence_threshold,
            save=False,
            verbose=False,
        )
        inference_ms = (perf_counter() - started_at) * 1000

        result = results[0]
        detections: list[Detection] = []
        names = result.names

        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())
                x1, y1, x2, y2 = [float(value) for value in box.xyxy[0].tolist()]
                detections.append(
                    Detection(
                        class_id=class_id,
                        class_name=str(names[class_id]),
                        confidence=confidence,
                        bbox_x1=x1,
                        bbox_y1=y1,
                        bbox_x2=x2,
                        bbox_y2=y2,
                    )
                )

        rendered = result.plot()
        result_image_path = self.settings.result_dir / f"{image_path.stem}_result.jpg"
        self._write_result_image(result_image_path, rendered)

        return DetectionResult(
            model_name=self.settings.yolo_model_name,
            inference_ms=round(inference_ms, 2),
            result_image_path=result_image_path,
            detections=detections,
        )

    @staticmethod
    def _write_result_image(path: Path, image_array) -> None:
        import cv2

        cv2.imwrite(str(path), image_array)


detector = YoloDetector()
