from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

ALLOWED_IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


async def save_upload_file(upload_dir: Path, file: UploadFile) -> Path:
    suffix = ALLOWED_IMAGE_TYPES.get(file.content_type or "")
    if suffix is None:
        raise ValueError("Only JPEG, PNG, and WEBP image files are supported.")

    filename = f"{uuid4().hex}{suffix}"
    destination = upload_dir / filename

    content = await file.read()
    destination.write_bytes(content)
    return destination
