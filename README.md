# Universal LLM Skill

一个为 Claude Code 设计的技能，通过单一、一致的 Python 接口提供对多个 LLM 提供商（OpenAI、Anthropic、Google Gemini 和 Kimi/月之暗面）的统一访问。

## 🌟 特性

- **多提供商支持**：通过统一接口调用 OpenAI GPT、Anthropic Claude、Google Gemini 和 Kimi（月之暗面）模型
- **一致的 API**：所有提供商使用相同的命令结构
- **JSON 响应格式**：标准化输出，便于解析
- **Token 使用追踪**：监控所有提供商的 token 消耗
- **完善的错误处理**：清晰的错误消息和状态码
- **中文语言优化**：Kimi 模型在中文任务上表现卓越

## 🚀 支持的提供商和模型

### OpenAI
- gpt-4o (GPT-4 Omni)
- gpt-4o-mini
- gpt-4-turbo
- gpt-3.5-turbo

### Anthropic
- claude-3-5-sonnet-20241022
- claude-3-5-haiku-20241022
- claude-3-opus-20240229

### Google Gemini
- gemini-1.5-pro
- gemini-1.5-flash
- gemini-pro

### Kimi (Moonshot AI / 月之暗面)
- moonshot-v1-8k (8K 上下文)
- moonshot-v1-32k (32K 上下文)
- moonshot-v1-128k (128K 上下文)
- kimi-k2 (万亿参数 MoE 模型)

## 📦 安装

1. **安装依赖**

```bash
pip install -r requirements.txt
```

2. **配置 API 密钥**

为你想使用的提供商设置环境变量：

```bash
export OPENAI_API_KEY='your-openai-key'
export ANTHROPIC_API_KEY='your-anthropic-key'
export GOOGLE_API_KEY='your-google-key'
export KIMI_API_KEY='your-kimi-key'
```

## 💡 使用方法

### 基本用法

```bash
python scripts/model_gateway.py \
  --provider "[PROVIDER]" \
  --model "[MODEL_NAME]" \
  --prompt "[YOUR_PROMPT]"
```

**参数说明:**
- `--provider`: 选择 `openai`、`anthropic`、`google` 或 `kimi`
- `--model`: 具体的模型名称
- `--prompt`: 你的提示词文本
- `--temperature`: (可选) 控制随机性，默认 0.7

### 使用示例

**OpenAI GPT-4:**
```bash
python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "Explain quantum computing"
```

**Claude 3.5 Sonnet:**
```bash
python scripts/model_gateway.py \
  --provider "anthropic" \
  --model "claude-3-5-sonnet-20241022" \
  --prompt "Write a Python sorting algorithm"
```

**Google Gemini:**
```bash
python scripts/model_gateway.py \
  --provider "google" \
  --model "gemini-1.5-pro" \
  --prompt "Generate creative story ideas" \
  --temperature 1.2
```

**Kimi (中文):**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-8k" \
  --prompt "请用中文解释量子计算的基本原理"
```

**Kimi 长上下文:**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-128k" \
  --prompt "分析这篇长文档..." \
  --temperature 0.3
```

## 📄 响应格式

**成功响应:**
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

**错误响应:**
```json
{
  "success": false,
  "error": "Detailed error message"
}
```

## 🎯 使用场景

- **模型对比**：在不同提供商之间测试相同的提示词
- **多提供商应用**：构建利用每个任务最佳模型的应用
- **成本优化**：根据预算和需求在模型之间切换
- **中文内容**：使用 Kimi 获得卓越的中文语言理解能力
- **长上下文任务**：利用 Kimi 的 128K 上下文窗口进行文档分析

## 🔑 获取 API 密钥

### OpenAI
访问: https://platform.openai.com/api-keys

### Anthropic
访问: https://console.anthropic.com/

### Google Gemini
访问: https://makersuite.google.com/app/apikey

### Kimi (月之暗面)
1. 访问: https://platform.moonshot.cn/console/account
2. 使用微信扫码登录
3. 创建 API Key
4. 新用户获赠 ¥10 + 50万 tokens！

## 📚 最佳实践

**模型选择:**
- GPT-4o: 通用任务，高质量推理
- Claude 3.5 Sonnet: 编程、分析、长上下文
- Gemini 1.5 Pro: 多模态任务，成本效益
- Kimi: 中文语言，超长上下文 (128K)

**Temperature 设置:**
- 0.0-0.3: 事实性、确定性
- 0.7: 平衡（默认）
- 1.0-2.0: 创造性、多样性

## 🛠️ 开发

### 文件结构
```
universal-llm-skill/
├── SKILL.md                 # Claude skill 文档
├── requirements.txt         # Python 依赖
├── scripts/
│   └── model_gateway.py    # 主网关脚本
└── README.md               # 本文件
```

### 贡献

欢迎贡献！请随时提交 issue 或 pull request。

## 📝 许可证

MIT License - 欢迎在你的项目中使用此技能！

## 🙏 致谢

- 为 [Claude Code](https://claude.com/claude-code) 构建
- 由 OpenAI、Anthropic、Google 和 Moonshot AI APIs 驱动

## 📮 支持

如果遇到任何问题或有疑问：
1. 查看 [SKILL.md](SKILL.md) 文档
2. 在 GitHub 上提交 issue
3. 查看错误消息 - 它们旨在提供帮助！

---

**用 ❤️ 为 Claude Code 社区打造**
