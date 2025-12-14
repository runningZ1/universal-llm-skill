# Universal LLM Skill

一个为 Claude Code 设计的 Kimi (月之暗面) 客户端技能，通过简洁的 Python 接口访问 Kimi 的所有模型系列。

## 🌟 特性

- **支持所有 Kimi 模型**：moonshot-v1-8k、moonshot-v1-32k、moonshot-v1-128k、kimi-k2
- **配置文件管理**：支持 .env 配置文件，API 密钥管理更安全
- **灵活调用**：可通过环境变量、配置文件或命令行参数设置
- **JSON 响应格式**：标准化输出，便于解析
- **Token 使用追踪**：监控每次调用的 token 消耗
- **完善的错误处理**：清晰的中文错误消息和状态码
- **中文语言优化**：Kimi 模型在中文任务上表现卓越

## 🚀 支持的模型

### Kimi (Moonshot AI / 月之暗面)

#### 通用对话模型
- **moonshot-v1-8k** (8K 上下文) - 适合通用任务，快速响应
- **moonshot-v1-32k** (32K 上下文) - 适合中等长度文档
- **moonshot-v1-128k** (128K 上下文) - 适合长文档分析

#### K2 系列（万亿参数 MoE 架构）
- **kimi-k2-thinking** (256K 上下文)
  - 深度推理模型，支持思维链输出（reasoning_content）
  - 推荐温度：1.0
  - 适合复杂推理、数学竞赛、编程任务、代理搜索

- **kimi-k2-instruct** (128K 上下文)
  - 快速响应模型，强大的工具调用能力
  - 推荐温度：0.6
  - 适合通用对话、工具编排、自主问题解决

## 📦 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

**方式 A：使用配置文件（推荐）**

复制示例配置文件：
```bash
cp config/.env.example config/.env
```

编辑 `config/.env` 并填入你的 API 密钥：
```bash
KIMI_API_KEY=your-kimi-api-key-here
DEFAULT_MODEL=moonshot-v1-8k
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4096
```

**方式 B：使用环境变量**

```bash
export KIMI_API_KEY='your-kimi-api-key-here'
```

**方式 C：命令行参数**

```bash
python scripts/kimi_client.py --api-key "your-key" --prompt "你好"
```

## 💡 使用方法

### 基本用法

```bash
# 使用默认配置
python scripts/kimi_client.py --prompt "你好，请介绍一下自己"

# 指定模型
python scripts/kimi_client.py --model moonshot-v1-128k --prompt "分析这篇长文档..."

# 自定义参数
python scripts/kimi_client.py \
  --model kimi-k2 \
  --prompt "复杂推理任务" \
  --temperature 0.3 \
  --max-tokens 2000
```

### 参数说明

- `--prompt` (必需): 发送给模型的提示词
- `--model` (可选): 模型名称，默认从配置文件读取或使用 moonshot-v1-8k
- `--temperature` (可选): 控制随机性 (0.0-2.0)，默认 0.7
- `--max-tokens` (可选): 最大生成 token 数，默认 4096
- `--api-key` (可选): API 密钥，优先级高于配置文件

### 使用示例

**示例 1：基本对话**
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

## 📄 响应格式

**成功响应（通用模型）:**
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

**成功响应（K2-Thinking 模型，包含思维链）:**
```json
{
  "success": true,
  "provider": "kimi",
  "model": "kimi-k2-thinking",
  "response": "最终答案...",
  "reasoning_content": "详细的思维推理过程...",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

**错误响应:**
```json
{
  "success": false,
  "error": "详细的错误消息"
}
```

## 🎯 使用场景

### 通用场景
- **中文内容处理**：Kimi 在中文理解和生成上表现卓越
- **长文档分析**：利用 128K/256K 上下文窗口处理整本书、长论文
- **代码理解**：分析大型代码库，提供重构建议
- **创意写作**：小说、剧本、诗歌创作
- **专业翻译**：中英文档翻译，保持专业术语准确性

### K2-Thinking 特色场景
- **复杂数学推理**：数学竞赛题目（AIME、HMMT）、证明题
- **深度代码分析**：代码审查、bug 修复（SWE-bench）、算法优化
- **代理搜索任务**：多步骤信息检索和整合（需要工具调用）
- **科学问题解答**：物理、化学、生物等专业领域问题
- **学术研究辅助**：处理学术论文，生成文献综述

### K2-Instruct 特色场景
- **快速问答**：日常对话、知识查询
- **工具编排**：多工具协同调用，自动化任务执行
- **代码生成**：快速原型开发、代码补全
- **自主问题解决**：独立完成复杂任务，无需人工干预

## 🔑 获取 API 密钥

### Kimi (月之暗面)
1. 访问: https://platform.moonshot.cn/console/account
2. 使用微信扫码登录
3. 在控制台中创建 API Key
4. 新用户获赠 **¥10 + 50万 tokens**！

## 📚 最佳实践

### 模型选择指南

| 模型 | 上下文 | 推荐温度 | 适用场景 | 特点 |
|------|--------|---------|---------|------|
| moonshot-v1-8k | 8K | 0.7 | 通用对话、简短任务 | 快速、成本低 |
| moonshot-v1-32k | 32K | 0.7 | 中等文档分析 | 平衡性能与成本 |
| moonshot-v1-128k | 128K | 0.7 | 长文档、整本书 | 超长上下文 |
| kimi-k2-thinking | 256K | 1.0 | 复杂推理、专业任务 | 深度思维，支持思维链 |
| kimi-k2-instruct | 128K | 0.6 | 工具调用、快速响应 | 强大工具编排 |

### Temperature 设置建议

#### 通用模型（moonshot-v1 系列）
- **0.0-0.3**: 事实性、确定性任务（翻译、总结、分析）
- **0.7**: 平衡创造力和一致性（默认值，通用对话）
- **1.0-2.0**: 创造性任务（写作、头脑风暴、创意生成）

#### K2 模型
- **kimi-k2-thinking**: 推荐 1.0（深度推理、数学竞赛、复杂问题）
- **kimi-k2-instruct**: 推荐 0.6（精确响应、工具调用、编程任务）

### Token 管理

- 响应中包含 `usage` 字段，可追踪每次调用的 token 消耗
- 不同模型定价不同，请查看官方定价页面
- 建议为长文档任务预留足够的 `max_tokens`

## 🛠️ 开发

### 文件结构
```
universal-llm-skill/
├── config/
│   ├── .env.example       # API 配置示例
│   └── .env              # 实际配置（不提交到 Git）
├── scripts/
│   └── kimi_client.py    # Kimi 客户端脚本
├── .gitignore
├── README.md             # 本文件
├── SKILL.md              # Claude Skill 文档
└── requirements.txt      # Python 依赖
```

### 贡献

欢迎贡献！请随时提交 issue 或 pull request。

建议贡献方向：
- 添加更多使用示例
- 改进错误处理
- 添加更多配置选项
- 性能优化

## 📝 许可证

MIT License - 欢迎在你的项目中使用此技能！

## 🙏 致谢

- 为 [Claude Code](https://claude.com/claude-code) 构建
- 由 [Moonshot AI（月之暗面）](https://www.moonshot.cn/) 提供 API 支持

## 📮 支持

如果遇到任何问题或有疑问：
1. 查看 [SKILL.md](SKILL.md) 文档获取详细使用说明
2. 在 GitHub 上提交 issue
3. 查看错误消息 - 它们旨在提供帮助！
4. 访问 [Kimi 官方文档](https://platform.moonshot.cn/docs)

---

**用 ❤️ 为 Claude Code 社区打造**
