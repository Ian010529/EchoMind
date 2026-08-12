"""Create an Anthropic-style async client for supported LLM providers."""
from types import SimpleNamespace
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI


class _OpenAIMessages:
    """Expose ``messages.create`` while using OpenAI's Responses API."""

    def __init__(self, client: AsyncOpenAI):
        self._client = client

    async def create(
        self,
        *,
        model: str,
        max_tokens: int,
        messages: List[Dict[str, Any]],
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        **_: Any,
    ) -> Any:
        request: Dict[str, Any] = {
            "model": model,
            "input": messages,
            "max_output_tokens": max_tokens,
        }
        if system:
            request["instructions"] = system
        if temperature is not None and not model.startswith("gpt-5"):
            request["temperature"] = temperature

        response = await self._client.responses.create(**request)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=response.output_text)]
        )


class OpenAIAnthropicCompat:
    """Small compatibility surface used by the existing EchoMind call sites."""

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.messages = _OpenAIMessages(
            AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=60.0)
        )


def create_llm_client(api_key: str, base_url: Optional[str] = None) -> Any:
    """Return an OpenAI Responses client or the existing Anthropic client."""
    hostname = urlparse(base_url).hostname if base_url else ""
    is_openai = bool(hostname and hostname.endswith("openai.com")) or api_key.startswith("sk-proj-")
    if is_openai:
        return OpenAIAnthropicCompat(api_key=api_key, base_url=base_url)

    kwargs: Dict[str, Any] = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return AsyncAnthropic(**kwargs)
