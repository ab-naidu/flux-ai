from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.gemini_service import analyze_delivery_image
from app.services.railtracks import trace

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze")
async def analyze(
    file: Annotated[UploadFile, File(description="Pallet + invoice image")],
) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload an image (jpg/png/webp)")
    raw = await file.read()
    if len(raw) > 12 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large (max 12MB)")
    mime = file.content_type.split(";")[0].strip()
    with trace("multimodal.analyze", {"filename": file.filename, "bytes": len(raw)}) as trace_id:
        try:
            result = analyze_delivery_image(raw, mime_type=mime)
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {e!s}") from e
        return {"trace_id": trace_id, **result}
