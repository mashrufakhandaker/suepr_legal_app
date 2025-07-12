# app/models/ai_models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class LegalProfile(BaseModel):
    name: str
    state: str
    case_type: str

class ComprehensiveCaseInput(BaseModel):
    prompt: str
    legal_profile: LegalProfile
    doc_text: Optional[str] = None
    message: Optional[str] = None

class TimelineStep(BaseModel):
    step: str
    due_date: str
    status: str = "pending"
    description: Optional[str] = None

class ComprehensiveCaseOutput(BaseModel):
    summary: str
    score: int
    strengths: List[str]
    weaknesses: List[str]
    followup_questions: List[str]
    recommended_court: str
    gameplan: List[str]
    timeline: List[TimelineStep]
    chat_response: Optional[str] = None

class UserDetails(BaseModel):
    name: str
    address: str
    opposing_party: str
    facts: str
    additional_info: Optional[str] = None
    tenant_name: Optional[str] = None
    landlord_name: Optional[str] = None
    amount: Optional[str] = None
    issue: Optional[str] = None

class LegalDocsInput(BaseModel):
    document_type: str
    case_summary: str
    user_details: UserDetails

class LegalDocsOutput(BaseModel):
    doc_title: str
    doc_content: str
    format: str = "docx"
    download_url: Optional[str] = None

class CaseInterpretOutput(BaseModel):
    extracted_text: str
    legal_summary: str
    actions: List[str]
    confidence_score: Optional[int] = None
