#!/usr/bin/env python3
"""
Kimi (Moonshot AI) 客户端
支持所有 Kimi 模型系列：
- moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k: 通用对话模型
- kimi-k2-thinking: 深度推理模型，支持思维链输出
- kimi-k2-instruct: 快速响应模型，适合工具调用和代理任务
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional


def load_config() -> Dict[str, str]:
    """从 .env 文件加载配置"""
    config = {}

    # 尝试从多个位置加载 .env 文件
    possible_paths = [
        Path(__file__).parent.parent / "config" / ".env",  # ../config/.env
        Path.cwd() / "config" / ".env",                     # ./config/.env
        Path.cwd() / ".env",                                # ./.env
    ]

    env_file = None
    for path in possible_paths:
        if path.exists():
            env_file = path
            break

    if env_file:
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            print(f"警告: 读取配置文件失败: {e}", file=sys.stderr)

    return config


def get_api_key(config: Dict[str, str]) -> Optional[str]:
    """获取 API Key（优先使用环境变量，其次使用配置文件）"""
    return os.getenv("KIMI_API_KEY") or config.get("KIMI_API_KEY")


def call_kimi(
    model: str,
    prompt: str,
    api_key: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    api_url: str = "https://api.moonshot.cn/v1/chat/completions"
) -> Dict[str, Any]:
    """调用 Kimi API"""
    try:
        import requests
    except ImportError:
        return {
            "success": False,
            "error": "requests 库未安装。请运行: pip install requests"
        }

    try:
        url = api_url

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()

        # 提取响应内容
        message = result["choices"][0]["message"]
        response_data = {
            "success": True,
            "provider": "kimi",
            "model": model,
            "response": message["content"],
            "usage": {
                "prompt_tokens": result.get("usage", {}).get("prompt_tokens"),
                "completion_tokens": result.get("usage", {}).get("completion_tokens"),
                "total_tokens": result.get("usage", {}).get("total_tokens")
            }
        }

        # K2-Thinking 模型会返回 reasoning_content（思维链）
        if "reasoning_content" in message and message["reasoning_content"]:
            response_data["reasoning_content"] = message["reasoning_content"]

        return response_data

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Kimi API 请求错误: {str(e)}"
        }
    except KeyError as e:
        return {
            "success": False,
            "error": f"响应解析错误: 缺少字段 {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Kimi API 错误: {str(e)}"
        }


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="Kimi (Moonshot AI) 客户端 - 支持所有 Kimi 模型系列",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的模型：
  moonshot-v1-8k      8K 上下文，适合通用任务
  moonshot-v1-32k     32K 上下文，适合中等长度文档
  moonshot-v1-128k    128K 上下文，适合长文档分析
  kimi-k2-thinking    256K 上下文，深度推理，支持思维链（推荐温度 1.0）
  kimi-k2-instruct    128K 上下文，快速响应，工具调用（推荐温度 0.6）

示例：
  %(prog)s --prompt "你好，请介绍一下自己"
  %(prog)s --model moonshot-v1-128k --prompt "分析这篇长文档..."
  %(prog)s --model kimi-k2-thinking --prompt "复杂推理任务" --temperature 1.0
        """
    )

    parser.add_argument(
        "--model",
        default=None,
        help="模型名称（默认: 从配置文件读取或使用 moonshot-v1-8k）"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="发送给模型的提示词"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="控制响应随机性（范围: 0.0-2.0，默认: 从配置文件读取或 0.7）"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="最大生成 token 数（默认: 从配置文件读取或 4096）"
    )
    parser.add_argument(
        "--api-key",
        help="Kimi API Key（可选，优先级高于配置文件）"
    )

    args = parser.parse_args()

    # 加载配置
    config = load_config()

    # 获取 API Key
    api_key = args.api_key or get_api_key(config)
    if not api_key:
        result = {
            "success": False,
            "error": "未找到 KIMI_API_KEY。请设置环境变量或在 config/.env 中配置"
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    # 获取模型（优先级：命令行参数 > 配置文件 > 默认值）
    model = args.model or config.get("DEFAULT_MODEL", "moonshot-v1-8k")

    # 获取 temperature（优先级：命令行参数 > 配置文件 > 默认值）
    if args.temperature is not None:
        temperature = args.temperature
    else:
        temperature = float(config.get("DEFAULT_TEMPERATURE", "0.7"))

    # 获取 max_tokens（优先级：命令行参数 > 配置文件 > 默认值）
    if args.max_tokens is not None:
        max_tokens = args.max_tokens
    else:
        max_tokens = int(config.get("MAX_TOKENS", "4096"))

    # 获取 API URL（优先级：环境变量 > 配置文件 > 默认值）
    api_url = os.getenv("KIMI_API_URL") or config.get("KIMI_API_URL", "https://api.moonshot.cn/v1/chat/completions")

    # 调用 API
    result = call_kimi(
        model=model,
        prompt=args.prompt,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        api_url=api_url
    )

    # 输出 JSON 响应
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 退出码
    sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    main()
