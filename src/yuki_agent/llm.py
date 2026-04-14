from __future__ import annotations


class SimpleLLM:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def generate(self, system_prompt: str, conversation: str, user_input: str) -> str:
        return (
            f"[{self.model_name}] mock response\n"
            f"system: {system_prompt}\n"
            f"context:\n{conversation}\n"
            f"user: {user_input}"
        )
