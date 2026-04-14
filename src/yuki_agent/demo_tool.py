from __future__ import annotations


class EchoTool:
    name = "echo"
    description = "Echo back the provided input."

    def run(self, input_text: str) -> str:
        return input_text if input_text else "empty input"
