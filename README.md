# Universal LLM Skill

A Claude Code skill that provides unified access to multiple LLM providers (OpenAI, Anthropic, Google Gemini, and Kimi/Moonshot) through a single, consistent Python interface.

## 🌟 Features

- **Multi-Provider Support**: Call OpenAI GPT, Anthropic Claude, Google Gemini, and Kimi (Moonshot) models from one unified interface
- **Consistent API**: Same command structure across all providers
- **JSON Response Format**: Standardized output for easy parsing
- **Token Usage Tracking**: Monitor token consumption for all providers
- **Comprehensive Error Handling**: Clear error messages and status codes
- **Chinese Language Optimization**: Kimi models excel at Chinese language tasks

## 🚀 Supported Providers & Models

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
- moonshot-v1-8k (8K context)
- moonshot-v1-32k (32K context)
- moonshot-v1-128k (128K context)
- kimi-k2 (Trillion-parameter MoE)

## 📦 Installation

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure API Keys**

Set environment variables for the providers you want to use:

```bash
export OPENAI_API_KEY='your-openai-key'
export ANTHROPIC_API_KEY='your-anthropic-key'
export GOOGLE_API_KEY='your-google-key'
export KIMI_API_KEY='your-kimi-key'
```

## 💡 Usage

### Basic Usage

```bash
python scripts/model_gateway.py \
  --provider "[PROVIDER]" \
  --model "[MODEL_NAME]" \
  --prompt "[YOUR_PROMPT]"
```

**Parameters:**
- `--provider`: Choose from `openai`, `anthropic`, `google`, or `kimi`
- `--model`: Specific model name
- `--prompt`: Your prompt text
- `--temperature`: (Optional) Controls randomness, default 0.7

### Examples

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

**Kimi (Chinese):**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-8k" \
  --prompt "请用中文解释量子计算的基本原理"
```

**Kimi Long Context:**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-128k" \
  --prompt "分析这篇长文档..." \
  --temperature 0.3
```

## 📄 Response Format

**Success Response:**
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

**Error Response:**
```json
{
  "success": false,
  "error": "Detailed error message"
}
```

## 🎯 Use Cases

- **Model Comparison**: Test the same prompt across different providers
- **Multi-Provider Applications**: Build apps that leverage the best model for each task
- **Cost Optimization**: Switch between models based on budget and requirements
- **Chinese Content**: Use Kimi for superior Chinese language understanding
- **Long Context Tasks**: Leverage Kimi's 128K context window for document analysis

## 🔑 Getting API Keys

### OpenAI
Visit: https://platform.openai.com/api-keys

### Anthropic
Visit: https://console.anthropic.com/

### Google Gemini
Visit: https://makersuite.google.com/app/apikey

### Kimi (Moonshot AI)
1. Visit: https://platform.moonshot.cn/console/account
2. Sign in with WeChat
3. Create API Key
4. New users get ¥10 + 500K tokens free!

## 📚 Best Practices

**Model Selection:**
- GPT-4o: General tasks, high-quality reasoning
- Claude 3.5 Sonnet: Coding, analysis, long contexts
- Gemini 1.5 Pro: Multimodal tasks, cost efficiency
- Kimi: Chinese language, ultra-long contexts (128K)

**Temperature Settings:**
- 0.0-0.3: Factual, deterministic
- 0.7: Balanced (default)
- 1.0-2.0: Creative, diverse

## 🛠️ Development

### File Structure
```
universal-llm-skill/
├── SKILL.md                 # Claude skill documentation
├── requirements.txt         # Python dependencies
├── scripts/
│   └── model_gateway.py    # Main gateway script
└── README.md               # This file
```

### Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📝 License

MIT License - Feel free to use this skill in your projects!

## 🙏 Acknowledgments

- Built for use with [Claude Code](https://claude.com/claude-code)
- Powered by OpenAI, Anthropic, Google, and Moonshot AI APIs

## 📮 Support

If you encounter any issues or have questions:
1. Check the [SKILL.md](SKILL.md) documentation
2. Open an issue on GitHub
3. Review the error messages - they're designed to be helpful!

---

**Made with ❤️ for the Claude Code community**
