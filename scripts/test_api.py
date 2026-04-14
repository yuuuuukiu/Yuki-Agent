from __future__ import annotations

import json
import sys

from yuki_agent.config import Settings
from yuki_agent.llm import SimpleLLM


def main() -> int:
    prompt = "你好，请只回复 OK。"
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])

    settings = Settings.from_env()
    print("provider:", settings.provider)
    print("model:", settings.model_name)
    print("base_url:", settings.base_url)
    print("api_key_configured:", bool(settings.api_key))

    llm = SimpleLLM(settings)
    try:
        reply = llm.generate(
            system_prompt=settings.system_prompt,
            conversation="",
            user_input=prompt,
        )
    except Exception as exc:
        print("status: failed")
        print("error:", exc)
        return 1

    print("status: ok")
    print("reply:")
    if isinstance(reply, str):
        print(reply)
    else:
        print(json.dumps(reply, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
