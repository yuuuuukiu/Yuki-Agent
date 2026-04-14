from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Tool(Protocol):
    name: str
    description: str

    def run(self, input_text: str) -> str:
        ...


@dataclass(slots=True)
class ToolRegistry:
    _tools: dict[str, Tool]

    def __init__(self) -> None:
        self._tools = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_descriptions(self) -> str:
        if not self._tools:
            return "No tools available."
        return "\n".join(
            f"- {tool.name}: {tool.description}" for tool in self._tools.values()
        )
