# vision-agent-backend-mvp

이미지 분석 결과를 저장하고 조회하는 비전 에이전트 백엔드 MVP입니다.  
사전학습 YOLO 모델을 FastAPI REST API에 연동해 이미지 업로드, 객체 탐지, 결과 이미지 저장, 탐지 메타데이터 조회 흐름을 구현했습니다.

## 목표

- 이미지 업로드 후 AI 추론을 수행하는 백엔드 API 구현
- 추론 결과를 DB에 저장하고 목록/상세 조회 API 제공
- 모델 추론 결과를 `class_name`, `confidence`, `bbox` 단위로 구조화
- Docker 기반 실행환경과 환경변수 기반 설정 제공

## 기술 스택

| 영역 | 기술 |
| --- | --- |
| Language | Python |
| API | FastAPI, Uvicorn |
| AI Inference | PyTorch 기반 Ultralytics YOLO |
| Database | SQLite, SQLAlchemy |
| Container | Docker, Docker Compose |
| Documentation | OpenAPI/Swagger, README |

## 주요 기능

- 이미지 업로드 및 객체 탐지 요청
- YOLO 추론 결과 JSON 변환
- 원본 이미지와 결과 이미지 경로 저장
- 이미지 분석 메타데이터 저장
- 분석 목록 조회
- 분석 상세 조회
- Swagger 기반 API 문서 자동 제공

## API 목록

| Method | Endpoint | 설명 |
| --- | --- | --- |
| GET | `/api/v1/health` | 서버 상태 확인 |
| POST | `/api/v1/analyses` | 이미지 업로드 및 YOLO 객체 탐지 |
| GET | `/api/v1/analyses` | 분석 결과 목록 조회 |
| GET | `/api/v1/analyses/{analysis_id}` | 분석 결과 상세 조회 |

Swagger 문서:

```text
http://localhost:8000/docs
```

## 데이터 구조

### image_analyses

| 필드 | 설명 |
| --- | --- |
| id | 분석 ID |
| original_filename | 업로드 원본 파일명 |
| stored_image_path | 저장된 원본 이미지 경로 |
| result_image_path | bbox가 표시된 결과 이미지 경로 |
| model_name | 사용한 모델명 |
| inference_ms | 추론 소요 시간 |
| created_at | 분석 생성 시각 |

### predictions

| 필드 | 설명 |
| --- | --- |
| id | 예측 ID |
| analysis_id | 분석 ID |
| class_id | 모델 클래스 ID |
| class_name | 탐지 클래스명 |
| confidence | 신뢰도 |
| bbox_x1, bbox_y1, bbox_x2, bbox_y2 | Bounding box 좌표 |

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker 실행

```bash
docker compose up --build
```

API 서버:

```text
http://localhost:8000
```

## EC2 배포

AWS EC2 Ubuntu 서버에 Docker Compose로 배포하는 절차는 [DEPLOYMENT.md](./DEPLOYMENT.md)에 정리했습니다.

배포 후 Swagger 문서:

```text
http://EC2_PUBLIC_IP:8000/docs
```

## 요청 예시

```bash
curl -X POST "http://localhost:8000/api/v1/analyses" \
  -F "file=@sample.jpg"
```

응답 예시:

```json
{
  "id": 1,
  "original_filename": "sample.jpg",
  "stored_image_path": "data/uploads/...",
  "result_image_path": "data/results/..._result.jpg",
  "model_name": "yolov8n.pt",
  "inference_ms": 120.5,
  "created_at": "2026-06-28T01:00:00",
  "predictions": [
    {
      "id": 1,
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.91,
      "bbox": {
        "x1": 10.2,
        "y1": 30.4,
        "x2": 250.7,
        "y2": 480.1
      }
    }
  ]
}
```

## 환경변수

`.env.example`을 참고해 설정할 수 있습니다.

| 변수 | 기본값 | 설명 |
| --- | --- | --- |
| DATABASE_URL | `sqlite:///./data/vision_agent.db` | DB 연결 정보 |
| UPLOAD_DIR | `./data/uploads` | 업로드 이미지 저장 경로 |
| RESULT_DIR | `./data/results` | 결과 이미지 저장 경로 |
| YOLO_MODEL_NAME | `yolov8n.pt` | 사용할 YOLO 모델 |
| CONFIDENCE_THRESHOLD | `0.35` | 탐지 confidence threshold |

## 한계와 개선점

- 현재는 단일 이미지 업로드만 지원하며, 영상 스트림/프레임 단위 분석은 추후 확장 필요
- 모델 학습은 포함하지 않고 사전학습 모델 추론만 연동
- 대용량 파일 처리, 재시도, 타임아웃, 비동기 Job 큐는 추가 개선 필요
- 데이터셋 버전 관리와 라벨 관리 기능은 별도 테이블로 확장 가능
- 운영 환경에서는 파일 저장소를 로컬 디스크에서 S3/Object Storage로 분리 필요

## 직무 연결 포인트

이 프로젝트는 AI 모델 자체 개발보다, AI 모델을 실제 서비스 백엔드에 통합하는 흐름에 초점을 두었습니다.  
이미지 입력, 모델 추론, 결과 저장, 메타데이터 조회 API를 구현하며 비전 에이전트 백엔드의 기본 구조를 실습했습니다.
