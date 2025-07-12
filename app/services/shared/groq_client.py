# groq_client.py
# app/services/shared/groq_client.py
import os
from groq import Groq
from typing import Optional, Dict, Any
import json

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        model: str = "llama3-8b-8192",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate a response using Groq API"""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    async def analyze_legal_document(self, text: str) -> Dict[str, Any]:
        """Analyze legal document and extract key information"""
        system_prompt = """You are a legal document analyzer. Analyze the provided text and extract:
        1. Document type (lease, notice, contract, etc.)
        2. Key parties involved
        3. Important dates
        4. Legal issues or concerns
        5. Recommended actions
        
        Return your analysis in a structured format."""
        
        response = await self.generate_response(
            prompt=f"Analyze this legal document:\n\n{text}",
            system_prompt=system_prompt,
            max_tokens=1500
        )
        
        return {"analysis": response}
    
    async def generate_legal_summary(self, case_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate case summary and recommendations"""
        system_prompt = """You are a legal case analyzer. Based on the provided case details, generate:
        1. A concise case summary
        2. Case strength score (1-100)
        3. Recommended court type
        4. Step-by-step gameplan
        5. Required documents
        
        Focus on practical, actionable advice."""
        
        prompt = f"""
        Case Details:
        User: {case_details.get('user_name', 'N/A')}
        State: {case_details.get('state', 'N/A')}
        Issue Type: {case_details.get('issue_type', 'N/A')}
        Description: {case_details.get('prompt', 'N/A')}
        
        Provide a comprehensive analysis and recommendations.
        """
        
        response = await self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1500
        )
        
        return {"summary": response}