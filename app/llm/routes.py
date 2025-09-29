import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.model import User
from app.auth_util import get_current_user
from app.global_constants import ErrorMessage, SuccessMessage
from app.llm.schema import TopicKeyword
from app.utils import get_response_schema

load_dotenv()

router = APIRouter(prefix="/llm", tags=["LLM"])

@router.post("/suggest-topics")
def suggest_topics(request: TopicKeyword, current_user: User = Depends(get_current_user)):

    keywords_list = request.topics
    keywords_str = ", ".join(keywords_list)  # "python, fastAPI, router"

    system_instruction = """You are an expert blog content assistant. Your task is to generate blog topics and points based on user-provided keywords. You must always return valid JSON in the specified format, with no extra text."""
    prompt = """Given the following keywords: [""" + keywords_str + """], generate 3 blog topics in a general blog style. Each topic should have exactly 3 points explaining what can be written about. All points should try to include the provided keywords where possible. Return strictly in this JSON format:\n\n[\n  {\n    \"topic\": \"Topic 1\",\n    \"points\": [\"Point 1\", \"Point 2\", \"Point 3\"]\n  },\n  {\n    \"topic\": \"Topic 2\",\n    \"points\": [\"Point 1\", \"Point 2\", \"Point 3\"]\n  },\n  {\n    \"topic\": \"Topic 3\",\n    \"points\": [\"Point 1\", \"Point 2\", \"Point 3\"]\n  }\n]\n\nDo not add any extra text outside the JSON array."""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Return a descriptive error for missing key in development
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ErrorMessage.SERVER_MISCONFIGURED.value)

    try:
        # Lazy import to avoid hard dependency at import time
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_completion_tokens=int(os.getenv("MAX_CONTEXT_TOKENS")),
            top_p=1
        )

        answer = (response.choices[0].message.content or "").strip()
        if not answer:
            answer = "The document does not contain that information."

        return get_response_schema(answer, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

    except Exception as exc:
        # Generic failure path per plan
        print("Exception occurred: ", exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=ErrorMessage.ANSWER_GENERATION_FAILED.value) from exc
