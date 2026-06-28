from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.analysis import ImageAnalysis, Prediction
from app.schemas.analysis import (
    AnalysisDetailResponse,
    AnalysisSummaryResponse,
    BoundingBox,
    HealthResponse,
    PredictionResponse,
)
from app.services.detector import detector
from app.services.storage import save_upload_file

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", app_name=settings.app_name)


@router.post(
    "/analyses",
    response_model=AnalysisDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_and_analyze(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> AnalysisDetailResponse:
    settings = get_settings()
    try:
        image_path = await save_upload_file(settings.upload_dir, file)
        detection_result = detector.analyze(image_path)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    analysis = ImageAnalysis(
        original_filename=file.filename or image_path.name,
        stored_image_path=str(image_path),
        result_image_path=str(detection_result.result_image_path),
        model_name=detection_result.model_name,
        inference_ms=detection_result.inference_ms,
    )
    analysis.predictions = [
        Prediction(
            class_id=item.class_id,
            class_name=item.class_name,
            confidence=item.confidence,
            bbox_x1=item.bbox_x1,
            bbox_y1=item.bbox_y1,
            bbox_x2=item.bbox_x2,
            bbox_y2=item.bbox_y2,
        )
        for item in detection_result.detections
    ]

    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return to_detail_response(analysis)


@router.get("/analyses", response_model=list[AnalysisSummaryResponse])
def list_analyses(db: Session = Depends(get_db)) -> list[AnalysisSummaryResponse]:
    analyses = db.scalars(
        select(ImageAnalysis).order_by(ImageAnalysis.created_at.desc())
    ).all()
    return [
        AnalysisSummaryResponse(
            id=item.id,
            original_filename=item.original_filename,
            model_name=item.model_name,
            inference_ms=item.inference_ms,
            prediction_count=len(item.predictions),
            created_at=item.created_at,
        )
        for item in analyses
    ]


@router.get("/analyses/{analysis_id}", response_model=AnalysisDetailResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)) -> AnalysisDetailResponse:
    analysis = db.get(ImageAnalysis, analysis_id)
    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found.")
    return to_detail_response(analysis)


def to_detail_response(analysis: ImageAnalysis) -> AnalysisDetailResponse:
    return AnalysisDetailResponse(
        id=analysis.id,
        original_filename=analysis.original_filename,
        stored_image_path=analysis.stored_image_path,
        result_image_path=analysis.result_image_path,
        model_name=analysis.model_name,
        inference_ms=analysis.inference_ms,
        created_at=analysis.created_at,
        predictions=[
            PredictionResponse(
                id=prediction.id,
                class_id=prediction.class_id,
                class_name=prediction.class_name,
                confidence=prediction.confidence,
                bbox=BoundingBox(
                    x1=prediction.bbox_x1,
                    y1=prediction.bbox_y1,
                    x2=prediction.bbox_x2,
                    y2=prediction.bbox_y2,
                ),
            )
            for prediction in analysis.predictions
        ],
    )
