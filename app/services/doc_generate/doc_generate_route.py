# app/services/doc_generate/doc_generate_route.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from app.models.ai_models import LegalDocsInput, LegalDocsOutput
from app.services.doc_generate.doc_generate_service import DocGenerateService

router = APIRouter()

def get_doc_generate_service():
    return DocGenerateService()

@router.post("/doc_generate", response_model=LegalDocsOutput)
async def generate_legal_document(
    input_data: LegalDocsInput,
    service: DocGenerateService = Depends(get_doc_generate_service)
):
    """Generate legal document"""
    try:
        return await service.generate_legal_document(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/doc_templates")
async def get_document_templates(
    service: DocGenerateService = Depends(get_doc_generate_service)
):
    """Get available document templates"""
    try:
        return await service.get_document_templates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
