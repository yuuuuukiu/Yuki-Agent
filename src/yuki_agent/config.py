from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    agent_name: str = "Yuki"
    system_prompt: str = "You are a helpful AI agent."
    model_name: str = "mock-model"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            agent_name=os.getenv("YUKI_AGENT_NAME", cls.agent_name),
            system_prompt=os.getenv("YUKI_SYSTEM_PROMPT", cls.system_prompt),
            model_name=os.getenv("YUKI_MODEL_NAME", cls.model_name),
        )
