---
name: universal-llm-skill
description: 当 Claude 需要调用 Kimi (月之暗面/Moonshot AI) 模型来生成中文响应、处理长文档或利用超长上下文能力时应使用此技能。此技能提供了访问 Kimi 所有模型系列的统一接口。
allowed-tools: Bash, Read
---

# Universal LLM Skill

## 概述

此技能提供了一个专门用于 Kimi (月之暗面/Moonshot AI) 的 Python 客户端，支持所有 Kimi 模型系列。通过统一的接口，可以轻松访问从 8K 到 128K 上下文长度的各种模型，无需管理复杂的 API 调用细节。

**主要优势：**
- 支持 Kimi 所有模型系列（moonshot-v1-8k/32k/128k, kimi-k2）
- 配置文件管理，API 密钥更安全
- 灵活的参数配置（环境变量、配置文件、命令行）
- 统一的 JSON 响应格式，便于解析
- Token 使用量追踪
- 完善的中文错误处理

## 何时使用此技能

在以下情况下使用此技能：
- 用户明确请求使用 Kimi 模型（例如，"使用 Kimi 分析这个"、"用月之暗面的模型处理"）
- 需要处理中文内容，利用 Kimi 的中文优化能力
- 需要超长上下文（最高 128K tokens）处理长文档、整本书
- 需要处理复杂的中文推理或创作任务
- 成本敏感的场景（Kimi 提供有竞争力的定价）

## 核心功能

该技能通过位于 `scripts/kimi_client.py` 的 Python 脚本提供对所有 Kimi 模型的访问。

### 支持的模型

| 模型 | 上下文长度 | 适用场景 |
|------|-----------|---------|
| moonshot-v1-8k | 8K | 通用对话、简短任务 |
| moonshot-v1-32k | 32K | 中等长度文档分析 |
| moonshot-v1-128k | 128K | 长文档、整本书分析 |
| kimi-k2 | 128K | 复杂推理、专业任务（万亿参数 MoE） |

## 环境设置

### 配置 API 密钥

脚本支持三种方式配置 API 密钥，按优先级排序：

**1. 命令行参数（最高优先级）**
```bash
python scripts/kimi_client.py --api-key "your-key" --prompt "你好"
```

**2. 环境变量**
```bash
export KIMI_API_KEY='your-kimi-api-key'
```

**3. 配置文件（推荐）**

复制示例配置：
```bash
cp config/.env.example config/.env
```

编辑 `config/.env`：
```bash
KIMI_API_KEY=your-kimi-api-key-here
DEFAULT_MODEL=moonshot-v1-8k
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4096
```

**获取 Kimi API 密钥：**
1. 访问月之暗面平台：https://platform.moonshot.cn/console/account
2. 使用微信或其他方式登录
3. 在控制台中创建 API Key
4. 新用户免费获得 ¥10 积分和 500,000 个 tokens

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 基本使用模式

```bash
python scripts/kimi_client.py --prompt "[YOUR_PROMPT]"
```

### 完整参数

```bash
python scripts/kimi_client.py \
  --model "[MODEL_NAME]" \
  --prompt "[YOUR_PROMPT]" \
  --temperature [0.0-2.0] \
  --max-tokens [NUMBER] \
  --api-key "[API_KEY]"
```

**参数说明：**
- `--prompt` (必需): 发送给模型的提示词
- `--model` (可选): 模型名称，默认从配置文件读取或 moonshot-v1-8k
- `--temperature` (可选): 控制响应随机性，默认 0.7
- `--max-tokens` (可选): 最大生成 token 数，默认 4096
- `--api-key` (可选): API 密钥，覆盖环境变量和配置文件

### 响应格式

**成功响应：**
```json
{
  "success": true,
  "provider": "kimi",
  "model": "moonshot-v1-8k",
  "response": "模型的文本响应...",
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
  "error": "详细的错误消息"
}
```

### 实际示例

**示例 1：使用默认配置**
```bash
python scripts/kimi_client.py --prompt "你好，请介绍一下自己"
```

**示例 2：长文档分析**
```bash
python scripts/kimi_client.py \
  --model moonshot-v1-128k \
  --prompt "分析这篇长文档的主要观点和论证结构..." \
  --temperature 0.3
```

**示例 3：使用最强模型**
```bash
python scripts/kimi_client.py \
  --model kimi-k2 \
  --prompt "请解释量子纠缠的本质，并给出数学推导"
```

**示例 4：创意写作**
```bash
python scripts/kimi_client.py \
  --model moonshot-v1-8k \
  --prompt "写一首关于春天的现代诗" \
  --temperature 1.2
```

## 工作流集成

### 典型使用流程

1. **准备配置** - 设置 API 密钥（配置文件或环境变量）
2. **选择模型** - 根据任务选择合适的模型
3. **执行脚本** - 运行 `kimi_client.py` 并传入提示词
4. **解析响应** - 提取 JSON 输出中的 `response` 字段
5. **监控使用** - 检查 `usage` 字段了解 token 消耗

### 在 Bash 中解析响应

```bash
# 存储完整响应
response=$(python scripts/kimi_client.py --prompt "你好")

# 提取响应文本
echo "$response" | python -c "import sys, json; print(json.load(sys.stdin)['response'])"

# 提取 token 使用情况
echo "$response" | python -c "import sys, json; print(json.load(sys.stdin)['usage'])"
```

## 错误处理

脚本提供清晰的中文错误消息：

- **缺少 API 密钥**: "未找到 KIMI_API_KEY。请设置环境变量或在 config/.env 中配置"
- **缺少库**: "requests 库未安装。请运行: pip install requests"
- **API 错误**: "Kimi API 请求错误: [详细错误信息]"
- **响应解析错误**: "响应解析错误: 缺少字段 [字段名]"

脚本在成功时以代码 0 退出，失败时以代码 1 退出。

## 最佳实践

### 模型选择指南

- **moonshot-v1-8k**: 日常对话、简短内容生成、快速响应场景
- **moonshot-v1-32k**: 中等长度文档分析、代码审查、技术文档
- **moonshot-v1-128k**: 长论文、整本书分析、大型代码库理解
- **kimi-k2**: 复杂推理、学术研究、专业领域任务

### Temperature 设置建议

- **0.0-0.3**: 翻译、总结、事实查询、数据分析
- **0.7**: 通用对话、问答、内容改写（默认值）
- **1.0-1.5**: 创意写作、头脑风暴、故事创作
- **1.5-2.0**: 极高创造性任务（可能降低连贯性）

### Token 管理

- 监控响应中的 `usage` 字段了解每次调用的成本
- 为长文档任务适当增加 `max_tokens` 值
- moonshot-v1-8k 最经济，适合批量处理
- 128K 模型虽然上下文大，但如果任务不需要长上下文，选择小模型更经济

### 配置文件最佳实践

- 将 `config/.env` 添加到 `.gitignore`（已配置）
- 为不同项目使用不同的配置文件
- 定期轮换 API 密钥以提高安全性
- 在配置文件中设置常用的默认值

## 限制

- 需要有效的 Kimi API 密钥
- 需要网络连接访问 Moonshot AI API
- 请求超时设置为 60 秒
- 不支持流式响应（未来可能添加）
- 不支持图像输入（Kimi 主要是文本模型）
- Token 限制由所选模型决定（8K/32K/128K）
