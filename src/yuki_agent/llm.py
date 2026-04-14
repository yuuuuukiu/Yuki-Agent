from __future__ import annotations

import json
import shlex
import subprocess
from typing import Any
from urllib import error, request

from yuki_agent.config import Settings


class SimpleLLM:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def generate(self, system_prompt: str, conversation: str, user_input: str) -> str:
        if self.settings.provider == "external_cli":
            return self._generate_with_external_cli(
                system_prompt=system_prompt,
                conversation=conversation,
                user_input=user_input,
            )

        return self._generate_with_openai_compatible(
            system_prompt=system_prompt,
            conversation=conversation,
            user_input=user_input,
        )

    def _generate_with_openai_compatible(
        self, system_prompt: str, conversation: str, user_input: str
    ) -> str:
        if not self.settings.api_key:
            raise ValueError("YUKI_API_KEY is required for openai_compatible mode.")

        base_url = self.settings.base_url.rstrip("/")
        endpoint = f"{base_url}/chat/completions"
        payload = {
            "model": self.settings.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": self._build_user_prompt(
                        conversation=conversation,
                        user_input=user_input,
                    ),
                },
            ],
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            endpoint,
            data=data,
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.settings.timeout_seconds) as response:
                body = response.read().decode("utf-8")
                status_code = getattr(response, "status", None)
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"LLM connection failed: {exc.reason}") from exc

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"LLM returned invalid JSON: {body}") from exc

        if isinstance(parsed, dict) and parsed.get("error"):
            raise RuntimeError(f"LLM error response: {parsed['error']}")

        choices = parsed.get("choices", []) if isinstance(parsed, dict) else []
        if not choices:
            raise RuntimeError(
                f"LLM returned no choices (HTTP {status_code}): {body}"
            )

        content = self._extract_choice_content(choices[0])
        if not content:
            raise RuntimeError(f"LLM returned empty content: {body}")
        return content

    def _generate_with_external_cli(
        self, system_prompt: str, conversation: str, user_input: str
    ) -> str:
        if not self.settings.external_command.strip():
            raise ValueError(
                "YUKI_EXTERNAL_COMMAND is required for external_cli mode."
            )

        prompt = (
            f"System:\n{system_prompt}\n\n"
            f"Conversation:\n{conversation}\n\n"
            f"User:\n{user_input}\n"
        )
        command = shlex.split(self.settings.external_command, posix=False)
        try:
            completed = subprocess.run(
                command,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=self.settings.timeout_seconds,
                check=True,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("External LLM command timed out.") from exc
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"External LLM command not found: {self.settings.external_command}"
            ) from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"External LLM command failed: {exc.stderr.strip() or exc.stdout.strip()}"
            ) from exc

        output = completed.stdout.strip()
        if not output:
            raise RuntimeError("External LLM command returned empty output.")
        return output

    @staticmethod
    def _build_user_prompt(conversation: str, user_input: str) -> str:
        if not conversation:
            return user_input
        return f"Conversation so far:\n{conversation}\n\nLatest user input:\n{user_input}"

    @staticmethod
    def _extract_choice_content(choice: dict[str, Any]) -> str:
        message = choice.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                text_parts: list[str] = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text")
                        if isinstance(text, str) and text:
                            text_parts.append(text)
                if text_parts:
                    return "\n".join(text_parts).strip()

        text = choice.get("text")
        if isinstance(text, str):
            return text.strip()

        delta = choice.get("delta")
        if isinstance(delta, dict):
            delta_content = delta.get("content")
            if isinstance(delta_content, str):
                return delta_content.strip()

        return ""
