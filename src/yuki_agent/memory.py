from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Message:
    role: str
    content: str


@dataclass(slots=True)
class ConversationMemory:
    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def as_prompt(self) -> str:
        lines: list[str] = []
        for message in self.messages:
            lines.append(f"{message.role}: {message.content}")
        return "\n".join(lines)
