import os
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from ports.outbound import LLMReasoningPort


class OpenAIReasoningAdapter(LLMReasoningPort):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "mock-key")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 0.3,
    ) -> str:
        try:
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
            }
            if response_format:
                kwargs["response_format"] = response_format
            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"[LLM ADAPTER ERROR] Chat completion call failed: {e}")
            raise e
