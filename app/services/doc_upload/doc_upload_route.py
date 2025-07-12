# app/services/doc_upload/doc_upload_route.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import os
from typing import Optional

from app.services.doc_upload.doc_upload_service import DocUploadService
from app.models.ai_models import CaseInterpretOutput
from app.core.config import settings

router = APIRouter()

def get_doc_upload_service():
    return DocUploadService()

@router.post("/doc", response_model=CaseInterpretOutput)
async def upload_document(
    file: UploadFile = File(...),
    case_id: Optional[str] = Form(None),
    service: DocUploadService = Depends(get_doc_upload_service)
):
    """Upload and process legal document"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File size too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Check file type
        allowed_extensions = ['.pdf', '.docx', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Process document
        result = await service.process_document(file_content, file.filename, case_id)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
