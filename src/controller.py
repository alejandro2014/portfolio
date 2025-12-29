from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool

from src.image_converter import ImageConverter

app = FastAPI()

MAX_UPLOAD_SIZE = 10 * 1024 * 1024 # 10 MB

@app.post("/simplify-image")
async def simplify_image(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpg", "image/jpeg"):
        raise HTTPException(status_code=400, detail="Only JPG images are supported")
    
    # Calculate size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File is too large")
    
    converter = ImageConverter()

    try:
        output_stream = await run_in_threadpool(converter.compress_image, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    return StreamingResponse(
        output_stream,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f'attachment; filename="simplified_{file.filename}"'
        }
    )