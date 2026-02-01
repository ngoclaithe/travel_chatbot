from fastapi import APIRouter, UploadFile, File, HTTPException, Request
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "static/uploads"

@router.post("/", response_model=dict)
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # secure_filename or just uuid
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Construct full URL
        # request.base_url provides scheme, host and port (e.g. http://localhost:8000/)
        # We need to be careful with double slashes if base_url ends with /
        base_url = str(request.base_url).rstrip("/")
        url = f"{base_url}/static/uploads/{unique_filename}"
        
        return {"url": url}
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
