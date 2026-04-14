# Yuki-Agent Template

一个最小可扩展的 Agent 智能体模板，适合作为原型起点。

## 包含内容

- `src/yuki_agent/agent.py`: Agent 主流程
- `src/yuki_agent/memory.py`: 简单对话记忆
- `src/yuki_agent/tools.py`: 工具协议和注册中心
- `src/yuki_agent/llm.py`: LLM 调用实现
- `src/yuki_agent/config.py`: 环境变量配置
- `src/yuki_agent/cli.py`: 命令行入口
- `src/yuki_agent/demo_tool.py`: 示例工具
- `scripts/test_api.py`: API 连通性测试脚本

## 快速开始

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python -m yuki_agent.cli
```

单独测试 API:

```bash
python scripts/test_api.py
python scripts/test_api.py 你好，请介绍一下自己
```

## 配置方式

### 1. OpenAI 兼容 API

`.env` 示例:

```env
YUKI_PROVIDER=openai_compatible
YUKI_MODEL_NAME=gpt-4o-mini
YUKI_API_KEY=your-api-key
YUKI_BASE_URL=https://api.openai.com/v1
```

兼容 OpenAI 协议的服务通常都只需要改这几个字段:

- `YUKI_PROVIDER=openai_compatible`
- `YUKI_MODEL_NAME=模型名`
- `YUKI_API_KEY=你的密钥`
- `YUKI_BASE_URL=服务商的 /v1 地址`

配置好后，可以先用下面的命令验证接口:

```bash
python scripts/test_api.py
```

### 2. 外部 CLI LLM

如果你想把推理直接交给本机安装的 `codex` 或 `claude`，可以先这样写:

```env
YUKI_PROVIDER=external_cli
YUKI_MODEL_NAME=codex
YUKI_EXTERNAL_COMMAND=codex exec --json
```

或:

```env
YUKI_PROVIDER=external_cli
YUKI_MODEL_NAME=claude
YUKI_EXTERNAL_COMMAND=claude --print
```

这种模式下，Agent 会把提示词交给外部命令处理。

## 下一步建议

1. 在 `.env` 中配置你的模型参数。
2. 将 `SimpleLLM.generate()` 替换成真实模型调用。
3. 按业务需要增加工具，例如搜索、数据库查询、自动化操作。
