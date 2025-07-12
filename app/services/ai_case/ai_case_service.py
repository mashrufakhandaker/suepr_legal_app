# app/services/ai_case/ai_case_service.py
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
import re
from app.services.shared.groq_client import GroqClient
from app.models.ai_models import (
    ComprehensiveCaseInput,
    ComprehensiveCaseOutput,
    TimelineStep,
)

class AICaseService:
    def __init__(self):
        self.groq_client = GroqClient()

    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """
        Extracts a JSON object from a string, even if it's embedded in other text.
        """
        # Find the start of the JSON object
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the response.")
        
        json_str = json_match.group(0)
        return json.loads(json_str)

    async def comprehensive_analysis(
        self, input_data: ComprehensiveCaseInput
    ) -> ComprehensiveCaseOutput:
        """
        Performs a comprehensive analysis of a legal case, including summary,
        scoring, and a game plan.
        """
        try:
            system_prompt = """
            You are a legal AI assistant. Based on the user's prompt, legal profile,
            and any provided document text, generate a comprehensive case analysis.
            The output should be a JSON object with the following structure:
            {
                "summary": "A brief summary of the case.",
                "score": "An integer score from 1-100 representing the case's strength.",
                "strengths": ["List of strengths of the case."],
                "weaknesses": ["List of weaknesses of the case."],
                "followup_questions": ["List of questions to ask the user for more information."],
                "recommended_court": "The recommended court for this case.",
                "gameplan": ["A list of steps to take."],
                "timeline": [
                    {"step": "Step 1", "due_date": "YYYY-MM-DD"},
                    {"step": "Step 2", "due_date": "YYYY-MM-DD"}
                ],
                "chat_response": "A response to the user's message, if provided."
            }
            """
            
            prompt = f"""
            User Prompt: {input_data.prompt}
            Legal Profile: {input_data.legal_profile.model_dump_json()}
            Document Text: {input_data.doc_text or "Not provided"}
            User Message: {input_data.message or "Not provided"}
            """

            response = await self.groq_client.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
            )
            
            analysis_result = self._extract_json_from_response(response)

            return ComprehensiveCaseOutput(**analysis_result)

        except (json.JSONDecodeError, ValueError) as e:
            # Handle cases where the response is not valid JSON
            raise Exception(f"Failed to decode the analysis response from the AI: {e}")
        except Exception as e:
            # Handle other potential errors
            raise Exception(f"An error occurred during comprehensive analysis: {e}")
