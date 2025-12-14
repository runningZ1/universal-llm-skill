---
name: universal-llm-skill
description: 当 Claude 需要调用外部 LLM API（OpenAI GPT 模型、Anthropic Claude 模型、Google Gemini 模型或 Kimi/月之暗面模型）来生成响应、比较输出或利用特定模型能力时应使用此技能。当用户明确请求使用不���的 LLM 提供商、想要比较模型输出或需要当前上下文中不可用的特定模型功能时使用此技能。
allowed-tools: Bash, Read
---

# Universal LLM Skill

## 概述

此技能提供了一个基于 Python 的统一网关，通过单一、一致的接口调用多个 LLM 提供商。该技能可以在 OpenAI（GPT 系列）、Anthropic（Claude 系列）、Google（Gemini 系列）和 Kimi（月之暗面系列）模型之间无缝切换，无需管理不同的 API 格式或认证方法。

**主要优势：**
- 跨四大主流 LLM 提供商的统一 API 接口
- 一致的 JSON 响应格式，便于解析
- 自动错误处理和信息丰富的错误消息
- 所有支持的提供商的 Token 使用追踪

## 何时使用此技能

在以下情况下使用此技能：
- 用户明确请求使用特定的 LLM 提供商（例如，"使用 GPT-4 分析这个"、"询问 Claude Opus 关于这个"、"将这个与 Gemini 的响应进行比较"、"使用 Kimi 处理这个"）
- 比较不同模型对相同提示的输出
- 利用特定模型的特定能力（例如，GPT-4 用于代码，Gemini 用于多模态任务，Kimi 用于长上下文中文内容）
- 跨不同提供商测试提示
- 需要使用与当前 Claude 实例不同的模型

## 核心功能

该技能通过位于 `scripts/model_gateway.py` 的单个 Python 脚本提供对多个 LLM 模型的访问。

### 支持的提供商和模型

**OpenAI:**
- gpt-4o (最新的 GPT-4 Omni)
- gpt-4o-mini (更小、更快的 GPT-4)
- gpt-4-turbo
- gpt-3.5-turbo
- 任何其他 OpenAI 聊天补全模型

**Anthropic:**
- claude-3-5-sonnet-20241022 (最新的 Claude 3.5 Sonnet)
- claude-3-5-haiku-20241022 (最新的 Claude 3.5 Haiku)
- claude-3-opus-20240229 (Claude 3 Opus)
- 任何其他 Anthropic messages API 模型

**Google:**
- gemini-1.5-pro (Gemini 1.5 Pro)
- gemini-1.5-flash (Gemini 1.5 Flash)
- gemini-pro (Gemini Pro)
- 任何其他 Google Generative AI 模型

**Kimi (Moonshot AI / 月之暗面):**
- moonshot-v1-8k (8K 上下文长度)
- moonshot-v1-32k (32K 上下文长度)
- moonshot-v1-128k (128K 上下文长度)
- kimi-k2 (万亿参数 MoE 模型，128K 上下文)
- 任何其他 Moonshot API 模型

## 环境设置

### 所需的 API 密钥

脚本需要将适当的 API 密钥设置为环境变量。必须至少配置以下其中一项：

- `OPENAI_API_KEY` - 用于 OpenAI 模型
- `ANTHROPIC_API_KEY` - 用于 Anthropic Claude 模型
- `GOOGLE_API_KEY` - 用于 Google Gemini 模型
- `KIMI_API_KEY` - 用于 Kimi（月之暗面）模型

**注意：** 只需设置正在使用的提供商的 API 密钥。如果在调用该提供商时缺少 API 密钥，脚本将返回清晰的错误消息。

**获取 Kimi API 密钥：**
1. 访问月之暗面平台：https://platform.moonshot.cn/console/account
2. 使用微信或其他方式登录
3. 在控制台中创建 API Key
4. 新用户免费获得 ¥10 积分和 500,000 个 tokens

### 安装依赖

首次使用前，请安装所需的 Python 包：

```bash
pip install -r requirements.txt
```

或根据需要单独安装：

```bash
pip install openai anthropic google-generativeai requests
```

## 使用说明

### 基本使用模式

要调用 LLM 模型，请使用以下必需参数执行 `model_gateway.py` 脚本：

```bash
python scripts/model_gateway.py \
  --provider "[PROVIDER]" \
  --model "[MODEL_NAME]" \
  --prompt "[YOUR_PROMPT]"
```

**必需参数：**
- `--provider`: 从 "openai"、"anthropic"、"google" 或 "kimi" 中选择
- `--model`: 指定确切的模型名称（例如，"gpt-4o"、"claude-3-5-sonnet-20241022"、"gemini-1.5-pro"、"moonshot-v1-8k"）
- `--prompt`: 要发送给模型的提示文本

**可选参数：**
- `--temperature`: 控制响应随机性（默认值：0.7，范围：0.0-2.0）

### 响应格式

脚本将 JSON 响应输出到 stdout，具有以下结构：

**成功响应：**
```json
{
  "success": true,
  "provider": "openai",
  "model": "gpt-4o",
  "response": "The model's text response...",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

**错误响应：**
```json
{
  "success": false,
  "error": "Detailed error message"
}
```

### 实际示例

**示例 1：调用 GPT-4 Omni**
```bash
python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "Explain quantum computing in simple terms"
```

**示例 2：调用 Claude 3.5 Sonnet**
```bash
python scripts/model_gateway.py \
  --provider "anthropic" \
  --model "claude-3-5-sonnet-20241022" \
  --prompt "Write a Python function to calculate Fibonacci numbers"
```

**示例 3：使用自定义 Temperature 调用 Gemini**
```bash
python scripts/model_gateway.py \
  --provider "google" \
  --model "gemini-1.5-pro" \
  --prompt "Generate creative story ideas" \
  --temperature 1.2
```

**示例 4：调用 Kimi（月之暗面）**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-8k" \
  --prompt "请用中文解释量子计算的基本原理"
```

**示例 5：使用长上下文调用 Kimi**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-128k" \
  --prompt "分析这篇长文档的主要观点..." \
  --temperature 0.3
```

**示例 6：比较输出（顺序调用）**
```bash
# 调用 GPT-4
python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "What is the capital of France?"

# 调用 Claude
python scripts/model_gateway.py \
  --provider "anthropic" \
  --model "claude-3-5-sonnet-20241022" \
  --prompt "What is the capital of France?"
```

## 工作流集成

### 典型使用流程

1. **确定需求** - 确定哪个 LLM 提供商和模型最适合任务
2. **检查环境** - 验证所需的 API 密钥是否已配置
3. **执行脚本** - 使用适当的参数运行 `model_gateway.py`
4. **解析响应** - 提取 JSON 输出并使用 `response` 字段
5. **处理错误** - 检查 `success` 字段并在需要时显示错误

### 在 Bash 中解析响应

在 Claude Code 中使用此技能时，捕获并解析 JSON 响应：

```bash
# 存储响应
response=$(python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "Hello, world!")

# 仅使用 Python 提取响应文本
echo "$response" | python -c "import sys, json; print(json.load(sys.stdin)['response'])"
```

## 错误处理

脚本为常见问题提供清晰的错误消息：

- **缺少 API 密钥**: "OPENAI_API_KEY environment variable not set"
- **缺少库**: "openai library not installed. Run: pip install openai"
- **API 错误**: "OpenAI API error: [detailed error message]"
- **无效提供商**: "Unknown provider: [provider_name]"

脚本在成功时以代码 0 退出，在失败时以代码 1 退出，便于在 shell 脚本中检查执行状态。

## 最佳实践

**模型选择指南：**
- 使用 GPT-4o 进行需要高质量和推理的通用任务
- 使用 Claude 3.5 Sonnet 进行编码、分析和长上下文任务
- 使用 Gemini 1.5 Pro 进行多模态任务或需要成本效益时
- 使用 Kimi（月之暗面）进行中文语言任务、长上下文处理（最多 128K）和成本效益高的替代方案
- 使用较小的模型（gpt-4o-mini、claude-3-5-haiku、gemini-1.5-flash、moonshot-v1-8k）进行更简单的任务

**Kimi 特定建议：**
- 使用 `moonshot-v1-8k` 进行通用中文语言任务
- 使用 `moonshot-v1-32k` 或 `moonshot-v1-128k` 进行长文档和上下文密集型任务
- 使用 `kimi-k2` 获得最先进的万亿参数模型能力
- Kimi 模型在中文语言理解和生成方面表现卓越

**Temperature 设置：**
- 使用 0.0-0.3 获得确定性、事实性响应
- 使用 0.7（默认）获得平衡的创造力和一致性
- 使用 1.0-2.0 获得创造性、多样化的输出

**Token 管理：**
- 监控响应中的 `usage` 字段以跟踪 token 消耗
- 请注意，不同的提供商有不同的定价模型
- 考虑对非常长的响应使用流式传输（此版本当前不支持）

## 限制

- 脚本不支持流式响应
- 目前未实现图像输入和多模态能力
- 没有内置的速率限制或重试逻辑
- 最大 token 限制是特定于提供商的，脚本不会强制执行
