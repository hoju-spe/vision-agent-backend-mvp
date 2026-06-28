from datetime import datetime

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class PredictionResponse(BaseModel):
    id: int
    class_id: int
    class_name: str
    confidence: float = Field(ge=0, le=1)
    bbox: BoundingBox


class AnalysisSummaryResponse(BaseModel):
    id: int
    original_filename: str
    model_name: str
    inference_ms: float
    prediction_count: int
    created_at: datetime


class AnalysisDetailResponse(BaseModel):
    id: int
    original_filename: str
    stored_image_path: str
    result_image_path: str | None
    model_name: str
    inference_ms: float
    created_at: datetime
    predictions: list[PredictionResponse]


class HealthResponse(BaseModel):
    status: str
    app_name: str
