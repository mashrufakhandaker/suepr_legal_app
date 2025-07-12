# app/services/ai_case/ai_case_route.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.ai_models import ComprehensiveCaseInput, ComprehensiveCaseOutput
from app.services.ai_case.ai_case_service import AICaseService

router = APIRouter()

def get_ai_case_service():
    return AICaseService()

@router.post("/case", response_model=ComprehensiveCaseOutput)
async def comprehensive_case_analysis(
    input_data: ComprehensiveCaseInput,
    service: AICaseService = Depends(get_ai_case_service)
):
    """
    Provides a comprehensive analysis of a legal case, including summary,
    scoring, and a game plan.
    """
    try:
        return await service.comprehensive_analysis(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
