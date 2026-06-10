import os
from typing import Optional
from enum import Enum


class LLMProvider(Enum):
    AZURE_OPENAI = "azure"
    CLAUDE = "claude"
    FALLBACK = "fallback"


class LLMConfig:

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "fallback").lower()
        if self.provider == "azure":
            self.setup_azure()
        elif self.provider == "claude":
            self.setup_claude()
        else:
            self.setup_fallback()

    def setup_azure(self):
        self.provider_type = LLMProvider.AZURE_OPENAI
        self.api_key = os.getenv("AZURE_OPENAI_KEY", "")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")
        self.api_version = "2024-02-15-preview"
        if not self.api_key or not self.endpoint:
            print("[LLM] Azure OpenAI credentials not found. Using fallback mode.")
            self.provider_type = LLMProvider.FALLBACK

    def setup_claude(self):
        self.provider_type = LLMProvider.CLAUDE
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
        if not self.api_key:
            print("[LLM] Anthropic credentials not found. Using fallback mode.")
            self.provider_type = LLMProvider.FALLBACK

    def setup_fallback(self):
        self.provider_type = LLMProvider.FALLBACK
        print("[LLM] Using fallback static responses mode (no API calls)")


llm_config = LLMConfig()


async def call_llm(
    prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7
) -> str:
    if llm_config.provider_type == LLMProvider.AZURE_OPENAI:
        return await call_azure_openai(prompt, system_prompt, temperature)
    elif llm_config.provider_type == LLMProvider.CLAUDE:
        return await call_claude(prompt, system_prompt, temperature)
    else:
        return get_static_response(prompt)


async def call_azure_openai(
    prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7
) -> str:
    try:
        from openai import AsyncAzureOpenAI

        client = AsyncAzureOpenAI(
            api_key=llm_config.api_key,
            api_version=llm_config.api_version,
            azure_endpoint=llm_config.endpoint,
        )
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await client.chat.completions.create(
            model=llm_config.deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Azure OpenAI error: {e}")
        return get_static_response(prompt)


async def call_claude(
    prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7
) -> str:
    try:
        from anthropic import AsyncAnthropic

        client = AsyncAnthropic(api_key=llm_config.api_key)
        response = await client.messages.create(
            model=llm_config.model,
            max_tokens=1500,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.content[0].text
    except Exception as e:
        print(f"Claude error: {e}")
        return get_static_response(prompt)


def get_static_response(prompt: str) -> str:
    if "auditor" in prompt.lower():
        return "Technical Analysis Report:\n- Soil conditions: Adequate drainage and 35% clay content supports corn cultivation\n- Water requirements: 550mm annual precipitation needed, current conditions sufficient\n- Frost risk assessment: Peak frost months July-August; recommend planting shift to December\n- Irrigation efficiency: Proposed investment of 60% would improve yield by 25-30%\n- Technical confidence: High"
    else:
        return "Strategic Assessment:\n- Scenario viability: Moderate with seasonal optimization\n- Decision triggers: Implement irrigation if water stress > 40%\n- Economic projections: +15% yield with optimal parameters\n- Resilience score: 72/100\n- Recommendations: Gradual implementation over 3 seasons"
