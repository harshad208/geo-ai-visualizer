import ollama
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class SearchContext(BaseModel):
    search_topic: Optional[str] = Field(
        None, description="A clean, optimized search engine query based on the user's request."
    )
    geographic_context: Optional[str] = Field(
        None, description="The specific country or continent mentioned in the query, if any."
    )

SYSTEM_PROMPT = """
You are an expert search query optimizer. Your task is to analyze the user's query
and extract two things: a clean search topic, and a geographic context (like a country or continent).

- If a specific country/continent is mentioned (e.g., 'India', 'USA', 'Europe'), extract it.
- If no specific region is mentioned, leave 'geographic_context' as null.
- The 'search_topic' should be a concise and effective search engine query.

Your entire response MUST be only a single, valid JSON object. Do not include any other text.
Follow this exact format:
{"search_topic": "...", "geographic_context": "..."}
"""

def extract_search_context(user_query: str) -> SearchContext:
    """
    Uses an LLM to extract a search topic and geographic context from a user query.
    """
    try:
        response = ollama.chat(
            model='phi3:mini',
            format='json',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_query},
            ]
        )
        response_json = json.loads(response['message']['content'])
        context_model = SearchContext(**response_json)
        print(f"LLM Search Context Extraction: {context_model.model_dump_json(indent=2)}")
        return context_model
    except (ValidationError, Exception) as e:
        print(f"Error during LLM context extraction: {e}")
        return SearchContext(search_topic=user_query, geographic_context=None)