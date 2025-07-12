# app/models/doc_models.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentUpload(BaseModel):
    filename: str
    file_type: str
    file_size: int
    upload_time: datetime
    case_id: Optional[str] = None

class DocumentProcessingResult(BaseModel):
    success: bool
    extracted_text: Optional[str] = None
    document_type: Optional[str] = None
    key_information: Optional[List[str]] = None
    error_message: Optional[str] = None