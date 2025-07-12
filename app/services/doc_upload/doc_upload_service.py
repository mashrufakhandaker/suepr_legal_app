# app/services/doc_upload/doc_upload_service.py
from typing import Dict, Any
import os
from datetime import datetime

from app.services.shared.groq_client import GroqClient
from app.services.shared.utils import FileUtils
from app.models.doc_models import DocumentProcessingResult
from app.models.ai_models import CaseInterpretOutput

class DocUploadService:
    def __init__(self):
        self.groq_client = GroqClient()
        self.file_utils = FileUtils()
    
    async def process_document(self, file_content: bytes, filename: str, case_id: str = None) -> CaseInterpretOutput:
        """Process uploaded document and extract legal information"""
        try:
            # Save file temporarily
            unique_filename = self.file_utils.generate_unique_filename(filename)
            file_path = await self.file_utils.save_upload_file(file_content, unique_filename)
            
            # Extract text based on file type
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext == '.pdf':
                extracted_text = await self.file_utils.extract_text_from_pdf(file_path)
            elif file_ext == '.docx':
                extracted_text = await self.file_utils.extract_text_from_docx(file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                extracted_text = await self.file_utils.extract_text_from_image(file_path)
            elif file_ext == '.txt':
                with open(file_path, 'r') as f:
                    extracted_text = f.read()
            else:
                raise Exception(f"Unsupported file type: {file_ext}")
            
            # Clean up temporary file
            await self.file_utils.cleanup_file(file_path)
            
            if not extracted_text.strip():
                raise Exception("No text could be extracted from the document")
            
            # Analyze document with AI
            analysis = await self.groq_client.analyze_legal_document(extracted_text)
            
            # Generate legal summary and actions
            system_prompt = """You are a legal document analyzer. Based on the document text, provide:
            1. A clear legal summary of what this document contains
            2. A list of recommended actions the user should take
            3. Important deadlines or dates mentioned
            4. Key legal issues or concerns
            
            Be practical and actionable in your recommendations."""
            
            prompt = f"""
            Document Analysis:
            {analysis.get('analysis', 'Document processed')}
            
            Extracted Text:
            {extracted_text[:2000]}...
            
            Provide a legal summary and recommended actions.
            """
            
            legal_summary = await self.groq_client.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1000
            )
            
            # Generate action items
            actions = [
                "Review document thoroughly",
                "Consult with attorney if needed",
                "Keep original document safe",
                "Note any important deadlines"
            ]
            
            # Try to extract specific actions from the summary
            if "respond" in legal_summary.lower():
                actions.insert(0, "Prepare written response")
            if "deadline" in legal_summary.lower():
                actions.insert(0, "Check all deadlines immediately")
            if "court" in legal_summary.lower():
                actions.insert(0, "Prepare for court proceedings")
            
            return CaseInterpretOutput(
                extracted_text=extracted_text,
                legal_summary=legal_summary,
                actions=actions[:5],  # Return top 5 actions
                confidence_score=85
            )
            
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    async def analyze_document_type(self, text: str) -> Dict[str, Any]:
        """Analyze document type and extract key information"""
        try:
            system_prompt = """Analyze this legal document and determine:
            1. Document type (lease, notice, contract, summons, etc.)
            2. Key parties involved
            3. Important dates and deadlines
            4. Legal significance
            5. Urgency level (Low/Medium/High)
            
            Return analysis in a structured format."""
            
            response = await self.groq_client.generate_response(
                prompt=f"Analyze this document:\n\n{text[:1500]}",
                system_prompt=system_prompt,
                max_tokens=800
            )
            
            return {
                "document_type": "Legal Document",
                "analysis": response,
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing document type: {str(e)}")
