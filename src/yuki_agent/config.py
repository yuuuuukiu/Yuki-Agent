from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return float(value)


@dataclass(slots=True)
class Settings:
    agent_name: str = "Yuki-Agent"
    system_prompt: str = "You are a helpful AI agent."
    provider: str = "openai_compatible"
    model_name: str = "gpt-4o-mini"
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    temperature: float = 0.7
    max_tokens: int = 1024
    timeout_seconds: int = 60
    external_command: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        defaults = cls()
        return cls(
            agent_name=_env_str("YUKI_AGENT_NAME", defaults.agent_name),
            system_prompt=_env_str("YUKI_SYSTEM_PROMPT", defaults.system_prompt),
            provider=_env_str("YUKI_PROVIDER", defaults.provider),
            model_name=_env_str("YUKI_MODEL_NAME", defaults.model_name),
            api_key=_env_str("YUKI_API_KEY", ""),
            base_url=_env_str("YUKI_BASE_URL", defaults.base_url),
            temperature=_env_float("YUKI_TEMPERATURE", defaults.temperature),
            max_tokens=_env_int("YUKI_MAX_TOKENS", defaults.max_tokens),
            timeout_seconds=_env_int(
                "YUKI_TIMEOUT_SECONDS", defaults.timeout_seconds
            ),
            external_command=_env_str("YUKI_EXTERNAL_COMMAND", ""),
        )
