#!/usr/bin/env python3
"""
LLM Skill Invoker Module

Invokes actual LLM skills via Claude Code SDK or direct API calls.
Supports multiple LLM providers and collects detailed metrics.
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class SkillInvoker:
    """Invokes skills via LLM API and collects metrics."""

    def __init__(self, provider: str = "anthropic", model: str = "claude-sonnet-4-20250514"):
        self.provider = provider
        self.model = model
        self.api_key = self._get_api_key(provider)
        self.base_url = self._get_base_url(provider)

    def _get_api_key(self, provider: str) -> str:
        """Get API key from environment."""
        key_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "azure": "AZURE_OPENAI_API_KEY"
        }
        key_name = key_map.get(provider, "ANTHROPIC_API_KEY")
        return os.environ.get(key_name, "")

    def _get_base_url(self, provider: str) -> str:
        """Get base API URL for provider."""
        url_map = {
            "anthropic": "https://api.anthropic.com/v1",
            "openai": "https://api.openai.com/v1",
            "google": "https://generativelanguage.googleapis.com/v1",
            "azure": "https://your-resource.openai.azure.com/openai"
        }
        return url_map.get(provider, "https://api.anthropic.com/v1")

    def invoke_skill(self, skill: Dict, test_input: Dict, skill_content: str = "") -> Dict:
        """
        Invoke a skill with test input and collect metrics.

        Args:
            skill: Skill metadata (id, name, path, etc.)
            test_input: Test case input (type, value)
            skill_content: Optional SKILL.md content for context

        Returns:
            Dict with output, metrics, and timing information
        """
        start_time = time.time()

        # Build skill system prompt from SKILL.md
        system_prompt = self._build_skill_prompt(skill, skill_content)

        # Build user message from test input
        user_message = self._build_user_message(test_input)

        # Invoke LLM
        try:
            if self.provider == "anthropic":
                result = self._invoke_anthropic(system_prompt, user_message)
            elif self.provider == "openai":
                result = self._invoke_openai(system_prompt, user_message)
            else:
                result = self._invoke_anthropic(system_prompt, user_message)  # Default

            response_time = time.time() - start_time

            return {
                "success": True,
                "output": result.get("content", ""),
                "response_time_s": round(response_time, 3),
                "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                "model": result.get("model", self.model),
                "raw_response": result
            }

        except Exception as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "output": f"Error: {str(e)}",
                "response_time_s": round(response_time, 3),
                "tokens_used": 0,
                "error": str(e)
            }

    def _build_skill_prompt(self, skill: Dict, skill_content: str) -> str:
        """Build system prompt from skill definition."""
        skill_name = skill.get("name", skill.get("id", "Unknown Skill"))
        skill_id = skill.get("id", "unknown")

        if skill_content:
            # Use actual SKILL.md content
            return f"""You are {skill_name} (ID: {skill_id}).

Follow the instructions and patterns defined in your skill definition below.

=== SKILL DEFINITION ===
{skill_content[:50000]}  # Truncate to avoid token limits
=== END SKILL DEFINITION ===

Apply this skill's methodology to analyze the user's request and provide a comprehensive, actionable response.
"""
        else:
            return f"""You are {skill_name}, an AI assistant specializing in this domain.

Provide comprehensive, accurate, and actionable responses based on your expertise.
"""

    def _build_user_message(self, test_input: Dict) -> str:
        """Build user message from test input."""
        input_type = test_input.get("type", "text")
        input_value = test_input.get("value", "")

        if input_type == "url":
            return f"""Please analyze this URL and provide your expert assessment:

URL: {input_value}

Apply your methodology systematically and provide actionable insights."""

        elif input_type == "code":
            return f"""Please analyze this code and provide your expert assessment:

```
{input_value}
```

Apply your methodology systematically and provide actionable insights."""

        elif input_type == "scenario":
            return f"""Please analyze this scenario and provide your expert assessment:

Scenario:
{input_value}

Apply your methodology systematically and provide actionable insights."""

        else:
            return f"""Please analyze the following and provide your expert assessment:

{input_value}

Apply your methodology systematically and provide actionable insights."""

    def _invoke_anthropic(self, system_prompt: str, user_message: str) -> Dict:
        """Invoke Anthropic Claude API."""
        import requests

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()
        return {
            "content": result.get("content", [{}])[0].get("text", ""),
            "usage": {
                "input_tokens": result.get("usage", {}).get("input_tokens", 0),
                "output_tokens": result.get("usage", {}).get("output_tokens", 0),
                "total_tokens": (
                    result.get("usage", {}).get("input_tokens", 0) +
                    result.get("usage", {}).get("output_tokens", 0)
                )
            },
            "model": result.get("model", self.model)
        }

    def _invoke_openai(self, system_prompt: str, user_message: str) -> Dict:
        """Invoke OpenAI API."""
        import requests

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()
        choice = result.get("choices", [{}])[0]
        return {
            "content": choice.get("message", {}).get("content", ""),
            "usage": result.get("usage", {}),
            "model": result.get("model", self.model)
        }


def invoke_skill_for_test(
    skill: Dict,
    test_case: Dict,
    skill_content: str = "",
    provider: str = "anthropic",
    model: str = "claude-sonnet-4-20250514"
) -> Dict:
    """
    Convenience function to invoke a skill for a test case.

    Args:
        skill: Skill metadata
        test_case: Test case definition
        skill_content: Optional SKILL.md content
        provider: LLM provider name
        model: Model identifier

    Returns:
        Test result dictionary
    """
    invoker = SkillInvoker(provider=provider, model=model)

    test_input = test_case.get("input", {})
    result = invoker.invoke_skill(skill, test_input, skill_content)

    # Add test metadata
    result["test_id"] = test_case.get("id", "unknown")
    result["test_name"] = test_case.get("name", "")
    result["skill_id"] = skill.get("id", "")

    return result
