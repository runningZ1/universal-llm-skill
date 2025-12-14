---
name: universal-llm-skill
description: This skill should be used when Claude needs to call external LLM APIs (OpenAI GPT models, Anthropic Claude models, Google Gemini models, or Kimi/Moonshot models) to generate responses, compare outputs, or leverage specific model capabilities. Use this skill when the user explicitly requests using a different LLM provider, wants to compare model outputs, or needs specific model features not available in the current context.
allowed-tools: Bash, Read
---

# Universal LLM Skill

## Overview

This skill provides a unified Python-based gateway to call multiple LLM providers through a single, consistent interface. The skill enables seamless switching between OpenAI (GPT series), Anthropic (Claude series), Google (Gemini series), and Kimi (Moonshot series) models without needing to manage different API formats or authentication methods.

**Key Benefits:**
- Unified API interface across four major LLM providers
- Consistent JSON response format for easy parsing
- Automatic error handling and informative error messages
- Token usage tracking for all supported providers

## When to Use This Skill

Use this skill when:
- The user explicitly requests using a specific LLM provider (e.g., "Use GPT-4 to analyze this", "Ask Claude Opus about this", "Compare this with Gemini's response", "Use Kimi to process this")
- Comparing outputs from different models for the same prompt
- Leveraging specific capabilities of a particular model (e.g., GPT-4 for code, Gemini for multimodal tasks, Kimi for long-context Chinese content)
- Testing prompts across different providers
- Needing to use a different model than the current Claude instance

## Core Functionality

The skill provides access to multiple LLM models through a single Python script located at `scripts/model_gateway.py`.

### Supported Providers and Models

**OpenAI:**
- gpt-4o (latest GPT-4 Omni)
- gpt-4o-mini (smaller, faster GPT-4)
- gpt-4-turbo
- gpt-3.5-turbo
- Any other OpenAI chat completion model

**Anthropic:**
- claude-3-5-sonnet-20241022 (latest Claude 3.5 Sonnet)
- claude-3-5-haiku-20241022 (latest Claude 3.5 Haiku)
- claude-3-opus-20240229 (Claude 3 Opus)
- Any other Anthropic messages API model

**Google:**
- gemini-1.5-pro (Gemini 1.5 Pro)
- gemini-1.5-flash (Gemini 1.5 Flash)
- gemini-pro (Gemini Pro)
- Any other Google Generative AI model

**Kimi (Moonshot AI / 月之暗面):**
- moonshot-v1-8k (8K context length)
- moonshot-v1-32k (32K context length)
- moonshot-v1-128k (128K context length)
- kimi-k2 (Trillion-parameter MoE model, 128K context)
- Any other Moonshot API model

## Environment Setup

### Required API Keys

The script requires appropriate API keys to be set as environment variables. At least one of the following must be configured:

- `OPENAI_API_KEY` - For OpenAI models
- `ANTHROPIC_API_KEY` - For Anthropic Claude models
- `GOOGLE_API_KEY` - For Google Gemini models
- `KIMI_API_KEY` - For Kimi (Moonshot) models

**Note:** Only the API key for the provider being used needs to be set. If an API key is missing when calling that provider, the script will return a clear error message.

**Getting Kimi API Key:**
1. Visit the Moonshot AI platform: https://platform.moonshot.cn/console/account
2. Sign in with WeChat or other methods
3. Create an API Key in the console
4. New users receive ¥10 credit and 500,000 tokens for free

### Installing Dependencies

Before first use, install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install individually as needed:

```bash
pip install openai anthropic google-generativeai requests
```

## Usage Instructions

### Basic Usage Pattern

To call an LLM model, execute the `model_gateway.py` script with the following required parameters:

```bash
python scripts/model_gateway.py \
  --provider "[PROVIDER]" \
  --model "[MODEL_NAME]" \
  --prompt "[YOUR_PROMPT]"
```

**Required Parameters:**
- `--provider`: Choose from "openai", "anthropic", "google", or "kimi"
- `--model`: Specify the exact model name (e.g., "gpt-4o", "claude-3-5-sonnet-20241022", "gemini-1.5-pro", "moonshot-v1-8k")
- `--prompt`: The prompt text to send to the model

**Optional Parameters:**
- `--temperature`: Controls response randomness (default: 0.7, range: 0.0-2.0)

### Response Format

The script outputs a JSON response to stdout with the following structure:

**Successful Response:**
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

### Practical Examples

**Example 1: Calling GPT-4 Omni**
```bash
python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "Explain quantum computing in simple terms"
```

**Example 2: Calling Claude 3.5 Sonnet**
```bash
python scripts/model_gateway.py \
  --provider "anthropic" \
  --model "claude-3-5-sonnet-20241022" \
  --prompt "Write a Python function to calculate Fibonacci numbers"
```

**Example 3: Calling Gemini with Custom Temperature**
```bash
python scripts/model_gateway.py \
  --provider "google" \
  --model "gemini-1.5-pro" \
  --prompt "Generate creative story ideas" \
  --temperature 1.2
```

**Example 4: Calling Kimi (Moonshot)**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-8k" \
  --prompt "请用中文解释量子计算的基本原理"
```

**Example 5: Calling Kimi with Long Context**
```bash
python scripts/model_gateway.py \
  --provider "kimi" \
  --model "moonshot-v1-128k" \
  --prompt "分析这篇长文档的主要观点..." \
  --temperature 0.3
```

**Example 6: Comparing Outputs (Sequential Calls)**
```bash
# Call GPT-4
python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "What is the capital of France?"

# Call Claude
python scripts/model_gateway.py \
  --provider "anthropic" \
  --model "claude-3-5-sonnet-20241022" \
  --prompt "What is the capital of France?"
```

## Workflow Integration

### Typical Usage Flow

1. **Identify the need** - Determine which LLM provider and model best suits the task
2. **Check environment** - Verify the required API key is configured
3. **Execute the script** - Run `model_gateway.py` with appropriate parameters
4. **Parse the response** - Extract the JSON output and use the `response` field
5. **Handle errors** - Check the `success` field and display errors if needed

### Parsing Responses in Bash

When using this skill from Claude Code, capture and parse the JSON response:

```bash
# Store the response
response=$(python scripts/model_gateway.py \
  --provider "openai" \
  --model "gpt-4o" \
  --prompt "Hello, world!")

# Extract just the response text using Python
echo "$response" | python -c "import sys, json; print(json.load(sys.stdin)['response'])"
```

## Error Handling

The script provides clear error messages for common issues:

- **Missing API Key**: "OPENAI_API_KEY environment variable not set"
- **Missing Library**: "openai library not installed. Run: pip install openai"
- **API Error**: "OpenAI API error: [detailed error message]"
- **Invalid Provider**: "Unknown provider: [provider_name]"

The script exits with code 0 on success and code 1 on failure, making it easy to check execution status in shell scripts.

## Best Practices

**Model Selection Guidelines:**
- Use GPT-4o for general tasks requiring high quality and reasoning
- Use Claude 3.5 Sonnet for coding, analysis, and long-context tasks
- Use Gemini 1.5 Pro for multimodal tasks or when cost efficiency is important
- Use Kimi (Moonshot) for Chinese language tasks, long-context processing (up to 128K), and cost-effective alternatives
- Use smaller models (gpt-4o-mini, claude-3-5-haiku, gemini-1.5-flash, moonshot-v1-8k) for simpler tasks

**Kimi-Specific Recommendations:**
- Use `moonshot-v1-8k` for general Chinese language tasks
- Use `moonshot-v1-32k` or `moonshot-v1-128k` for long documents and context-heavy tasks
- Use `kimi-k2` for the most advanced trillion-parameter model capabilities
- Kimi models excel at Chinese language understanding and generation

**Temperature Settings:**
- Use 0.0-0.3 for deterministic, factual responses
- Use 0.7 (default) for balanced creativity and consistency
- Use 1.0-2.0 for creative, diverse outputs

**Token Management:**
- Monitor the `usage` field in responses to track token consumption
- Be aware that different providers have different pricing models
- Consider using streaming for very long responses (not currently supported in this version)

## Limitations

- The script does not support streaming responses
- Image inputs and multimodal capabilities are not currently implemented
- No built-in rate limiting or retry logic
- Maximum token limits are provider-specific and not enforced by the script
