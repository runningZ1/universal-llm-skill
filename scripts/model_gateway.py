#!/usr/bin/env python3
"""
Universal LLM Client - Model Gateway Script
Provides a unified interface to call OpenAI, Anthropic Claude, Google Gemini, and Kimi (Moonshot) APIs.
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any


def call_openai(model: str, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
    """Call OpenAI API using the chat completions endpoint."""
    try:
        from openai import OpenAI
    except ImportError:
        return {
            "error": "openai library not installed. Run: pip install openai",
            "success": False
        }

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "error": "OPENAI_API_KEY environment variable not set",
            "success": False
        }

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )

        return {
            "success": True,
            "provider": "openai",
            "model": model,
            "response": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        return {
            "error": f"OpenAI API error: {str(e)}",
            "success": False
        }


def call_anthropic(model: str, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
    """Call Anthropic Claude API using the messages endpoint."""
    try:
        from anthropic import Anthropic
    except ImportError:
        return {
            "error": "anthropic library not installed. Run: pip install anthropic",
            "success": False
        }

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "error": "ANTHROPIC_API_KEY environment variable not set",
            "success": False
        }

    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "success": True,
            "provider": "anthropic",
            "model": model,
            "response": response.content[0].text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    except Exception as e:
        return {
            "error": f"Anthropic API error: {str(e)}",
            "success": False
        }


def call_google(model: str, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
    """Call Google Gemini API using the generative AI endpoint."""
    try:
        import google.generativeai as genai
    except ImportError:
        return {
            "error": "google-generativeai library not installed. Run: pip install google-generativeai",
            "success": False
        }

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "error": "GOOGLE_API_KEY environment variable not set",
            "success": False
        }

    try:
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": 4096,
        }

        model_instance = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config
        )

        response = model_instance.generate_content(prompt)

        return {
            "success": True,
            "provider": "google",
            "model": model,
            "response": response.text,
            "usage": {
                "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                "candidates_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
                "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
            }
        }
    except Exception as e:
        return {
            "error": f"Google API error: {str(e)}",
            "success": False
        }


def call_kimi(model: str, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
    """Call Kimi (Moonshot) API using the chat completions endpoint."""
    try:
        import requests
    except ImportError:
        return {
            "error": "requests library not installed. Run: pip install requests",
            "success": False
        }

    api_key = os.getenv("KIMI_API_KEY")
    if not api_key:
        return {
            "error": "KIMI_API_KEY environment variable not set",
            "success": False
        }

    try:
        url = "https://api.moonshot.cn/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 4096
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()

        return {
            "success": True,
            "provider": "kimi",
            "model": model,
            "response": result["choices"][0]["message"]["content"],
            "usage": {
                "prompt_tokens": result.get("usage", {}).get("prompt_tokens"),
                "completion_tokens": result.get("usage", {}).get("completion_tokens"),
                "total_tokens": result.get("usage", {}).get("total_tokens")
            }
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Kimi API request error: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"Kimi API error: {str(e)}",
            "success": False
        }


def main():
    """Main entry point for the model gateway."""
    parser = argparse.ArgumentParser(
        description="Universal LLM Client - Call OpenAI, Anthropic, Google, or Kimi models"
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=["openai", "anthropic", "google", "kimi"],
        help="LLM provider to use"
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Model name (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022', 'gemini-1.5-pro', 'moonshot-v1-8k')"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Prompt to send to the model"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for response randomness (default: 0.7)"
    )

    args = parser.parse_args()

    # Route to appropriate provider
    if args.provider == "openai":
        result = call_openai(args.model, args.prompt, args.temperature)
    elif args.provider == "anthropic":
        result = call_anthropic(args.model, args.prompt, args.temperature)
    elif args.provider == "google":
        result = call_google(args.model, args.prompt, args.temperature)
    elif args.provider == "kimi":
        result = call_kimi(args.model, args.prompt, args.temperature)
    else:
        result = {
            "error": f"Unknown provider: {args.provider}",
            "success": False
        }

    # Output JSON response to stdout
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Exit with appropriate code
    sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    main()
