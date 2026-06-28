# 이력서 작성 초안

## 보유 기술 및 역량

| 직무 | 보유 기술, 툴 | 역량 |
| --- | --- | --- |
| Back-end | Java, Spring Boot, JPA, REST API, MariaDB, RabbitMQ | 중급 |
| Back-end / AI Service | Python, FastAPI, SQLAlchemy, SQLite, PyTorch/YOLO | 초급 |
| Infra / Collaboration | Docker, Docker Compose, Git, GitHub, Linux 기본 명령어 | 초급~중급 |
| Front-end | React, Axios, Chart.js | 초급 |
| AI Tool | Claude Code, Cursor, ChatGPT | 중급 |

## 프로젝트 경험 대표 사례 2건

| 프로젝트명 | 역할 | 사용기술 | 기간 |
| --- | --- | --- | --- |
| LLM 기반 이메일 AI 에이전트 백엔드 | 백엔드 개발 | Java, Spring Boot, JPA, MariaDB, RabbitMQ, Docker | 2026.03.~2026.04. |
| vision-agent-backend-mvp | 백엔드 개발 | Python, FastAPI, PyTorch/YOLO, SQLite, Docker | 2026.06. |

## 지원동기 500자 이내

노타의 비전 에이전트 백엔드 직무는 AI 모델을 실제 서비스에서 활용할 수 있도록 데이터, 추론 결과, 운영 API를 안정적으로 연결하는 역할이라는 점에서 관심을 갖게 되었습니다. 저는 이메일 AI 에이전트 프로젝트에서 학습 Job, 데이터셋 버전, 모델 메타데이터를 관리하는 백엔드 구현을 경험했고, 이를 보완하기 위해 Python/FastAPI 기반 이미지 분석 API를 직접 구현했습니다. AI 모델 자체 개발보다는 모델이 제품 안에서 동작하도록 백엔드 구조를 만드는 일에 강점을 쌓고 싶습니다.

## 직무 관련 경험 1,000자 이내

LLM 기반 이메일 AI 에이전트 프로젝트에서 백엔드 개발을 맡아 AI 학습 및 운영 흐름을 관리하는 API를 구현했습니다. 학습 요청을 Job 단위로 저장하고, 데이터셋 버전과 모델 메타데이터를 별도 엔티티로 관리하며, AI worker의 학습 완료 이벤트를 RabbitMQ로 수신해 Job 상태와 모델 성능 지표를 갱신하는 구조를 경험했습니다. 이 과정에서 AI 엔지니어가 담당한 Python 기반 파이프라인과 서비스 백엔드 사이의 인터페이스를 이해하고, 결과를 운영자가 추적할 수 있는 데이터 구조로 저장하는 데 집중했습니다.

또한 노타의 비전 에이전트 직무와 직접 연결되는 역량을 보완하기 위해 `vision-agent-backend-mvp`를 구현했습니다. Python, FastAPI, PyTorch 기반 YOLO 모델을 사용해 이미지 업로드, 객체 탐지, 결과 이미지 저장, 탐지 메타데이터 조회 API를 구성했습니다. SQLite와 SQLAlchemy로 이미지 분석 결과와 bbox, confidence, class_name을 저장하고, Docker 기반 실행환경과 Swagger 문서를 제공했습니다. 이를 통해 이미지 입력부터 AI 추론, 결과 저장/조회까지 이어지는 비전 분석 백엔드의 기본 흐름을 실습했습니다.

## 문제해결 및 도전 경험 500자 이내

AI 에이전트 프로젝트에서 백엔드가 무거운 학습 처리까지 직접 담당하면 서버 부하와 운영 복잡도가 커질 수 있다는 문제가 있었습니다. 이를 해결하기 위해 백엔드는 Job 생성, 상태 관리, 결과 수신에 집중하고 실제 학습/배포 작업은 외부 실행 환경과 연동하는 방향으로 구조를 분리했습니다. 또한 학습 결과를 RabbitMQ 이벤트로 수신해 성공/실패 상태와 모델 지표를 갱신하도록 구현하며, AI 기능이 운영 관점에서 추적 가능하도록 개선했습니다.

## 기대 성과 목표 500자 이내

인턴십 기간 동안 Python 기반 백엔드와 비전 AI 파이프라인 연동 역량을 빠르게 끌어올리고 싶습니다. 기존에는 Java/Spring 중심으로 백엔드를 개발했지만, FastAPI와 YOLO 기반 미니 프로젝트를 통해 이미지 분석 API의 기본 흐름을 학습했습니다. 노타에서는 AI 엔지니어, 프론트엔드 엔지니어, PM과 협업하며 추론 결과 저장/조회 API, 데이터 관리 구조, 운영 어드민 API를 구현하는 데 기여하고 싶습니다.
