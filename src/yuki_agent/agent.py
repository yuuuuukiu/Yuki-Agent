from __future__ import annotations

from yuki_agent.config import Settings
from yuki_agent.llm import SimpleLLM
from yuki_agent.memory import ConversationMemory
from yuki_agent.tools import ToolRegistry


class Agent:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.memory = ConversationMemory()
        self.tools = ToolRegistry()
        self.llm = SimpleLLM(model_name=settings.model_name)

    def register_tool(self, tool: object) -> None:
        self.tools.register(tool)

    def run(self, user_input: str) -> str:
        if user_input.startswith("/tool "):
            return self._run_tool_command(user_input)

        self.memory.add("user", user_input)
        reply = self.llm.generate(
            system_prompt=self.settings.system_prompt,
            conversation=self.memory.as_prompt(),
            user_input=user_input,
        )
        self.memory.add("assistant", reply)
        return reply

    def _run_tool_command(self, command: str) -> str:
        parts = command.split(" ", 2)
        if len(parts) < 2:
            return "Usage: /tool <name> [input]"

        tool_name = parts[1]
        tool_input = parts[2] if len(parts) > 2 else ""
        tool = self.tools.get(tool_name)
        if tool is None:
            return f"Tool '{tool_name}' not found.\n{self.tools.list_descriptions()}"

        result = tool.run(tool_input)
        self.memory.add("tool", f"{tool_name}: {result}")
        return result
