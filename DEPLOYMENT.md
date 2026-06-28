# EC2 Docker Deployment Guide

이 문서는 `vision-agent-backend-mvp`를 AWS EC2 Ubuntu 서버에 Docker Compose로 배포하는 절차입니다.

## 1. GitHub에 레포 업로드

로컬 프로젝트 폴더에서:

```bash
git init
git add .
git commit -m "Initial commit: vision agent backend mvp"
git branch -M main
git remote add origin https://github.com/hoju-spe/vision-agent-backend-mvp.git
git push -u origin main
```

`origin` URL은 실제 GitHub 레포 주소로 바꿔야 합니다.

## 2. EC2 인스턴스 생성

권장 설정:

| 항목 | 값 |
| --- | --- |
| AMI | Ubuntu Server 22.04 LTS |
| Instance type | t2.micro 또는 t3.micro |
| Storage | 20GB 이상 권장 |
| Key pair | 새 키 생성 후 `.pem` 저장 |

YOLO/PyTorch 의존성 때문에 무료 티어 인스턴스에서는 첫 빌드와 첫 추론이 느릴 수 있습니다. 메모리 부족이 나면 swap 설정 또는 더 큰 인스턴스가 필요합니다.

## 3. 보안 그룹 설정

Inbound rule:

| Type | Port | Source |
| --- | --- | --- |
| SSH | 22 | My IP |
| Custom TCP | 8000 | My IP 또는 테스트용 `0.0.0.0/0` |

포트 `8000`을 전체 공개로 오래 열어두는 것은 권장하지 않습니다. 테스트가 끝나면 My IP로 제한하거나 인스턴스를 중지하세요.

## 4. EC2 접속

macOS/Linux:

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@EC2_PUBLIC_IP
```

Windows PowerShell:

```powershell
ssh -i C:\path\to\your-key.pem ubuntu@EC2_PUBLIC_IP
```

## 5. 서버 초기 설정

EC2 접속 후:

```bash
git clone https://github.com/hoju-spe/vision-agent-backend-mvp.git
cd vision-agent-backend-mvp
chmod +x deploy/ec2-setup.sh
./deploy/ec2-setup.sh
```

스크립트가 끝나면 Docker 권한 적용을 위해 SSH 연결을 끊고 다시 접속합니다.

```bash
exit
ssh -i your-key.pem ubuntu@EC2_PUBLIC_IP
cd vision-agent-backend-mvp
```

## 6. Docker Compose 실행

```bash
docker compose up -d --build
```

로그 확인:

```bash
docker compose logs -f
```

상태 확인:

```bash
docker compose ps
```

## 7. 접속 확인

브라우저에서:

```text
http://EC2_PUBLIC_IP:8000/docs
```

Health API:

```bash
curl http://EC2_PUBLIC_IP:8000/api/v1/health
```

## 8. 이미지 분석 테스트

서버에 테스트 이미지를 올린 뒤:

```bash
curl -X POST "http://EC2_PUBLIC_IP:8000/api/v1/analyses" \
  -F "file=@sample.jpg"
```

분석 목록:

```bash
curl http://EC2_PUBLIC_IP:8000/api/v1/analyses
```

## 9. 운영 중지

```bash
docker compose down
```

AWS 과금을 막으려면 테스트 후 EC2 인스턴스를 중지하거나 종료하세요.

## 지원서 표현 예시

Python/FastAPI 기반 이미지 분석 API를 구현하고 Docker Compose로 Linux 서버 환경에 배포했습니다. 이미지 업로드, YOLO 추론, 결과 메타데이터 저장/조회 API를 구성하며 AI 모델을 서비스 백엔드로 제공하는 흐름을 경험했습니다.
