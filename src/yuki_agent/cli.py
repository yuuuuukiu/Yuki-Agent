from __future__ import annotations

from yuki_agent.agent import Agent
from yuki_agent.config import Settings
from yuki_agent.demo_tool import EchoTool


def main() -> None:
    settings = Settings.from_env()
    agent = Agent(settings)
    agent.register_tool(EchoTool())

    print(f"{settings.agent_name} is ready. Type 'exit' to quit.")
    print("Use '/tool echo hello' to call a sample tool.")

    while True:
        user_input = input("You> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye.")
            break
        if not user_input:
            continue

        reply = agent.run(user_input)
        print(f"{settings.agent_name}> {reply}")


if __name__ == "__main__":
    main()
