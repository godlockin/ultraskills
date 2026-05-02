#!/usr/bin/env python3
"""
LLM Judge Module

Independent LLM-based evaluation of skill outputs.
Provides detailed quality scoring with rubric-based assessment.
"""

import json
import os
from typing import Dict, Any, List


class LLMJudge:
    """Evaluates skill outputs using LLM with detailed rubrics."""

    def __init__(self, provider: str = "anthropic", model: str = ""):
        self.provider = provider
        if not model:
            model = os.environ.get("SKILL_ARENA_MODEL", "")
        if not model:
            model = "gemini-2.5-flash" if provider == "google" else "claude-sonnet-4-20250514"
        self.model = model
        self.api_key = self._get_api_key(provider)

    def _get_api_key(self, provider: str) -> str:
        """Get API key from environment."""
        key_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY"
        }
        key_name = key_map.get(provider, "ANTHROPIC_API_KEY")
        return os.environ.get(key_name, "")

    def evaluate(
        self,
        test_case: Dict,
        skill_output: str,
        skill_name: str,
        rubric: Dict = None
    ) -> Dict:
        """
        Evaluate a skill's output against test criteria.

        Args:
            test_case: Test case definition with expected_outputs
            skill_output: The actual output from the skill
            skill_name: Name of the skill being evaluated
            rubric: Optional custom rubric

        Returns:
            Evaluation result with scores and rationale
        """
        # Build evaluation prompt
        prompt = self._build_eval_prompt(test_case, skill_output, skill_name, rubric)

        # Invoke LLM for evaluation
        eval_result = self._invoke_llm(prompt)

        # Parse evaluation result
        parsed = self._parse_evaluation(eval_result)

        return {
            "test_id": test_case.get("id", "unknown"),
            "test_name": test_case.get("name", ""),
            "skill_name": skill_name,
            "overall_score": parsed.get("overall_score", 5.0),
            "dimension_scores": parsed.get("dimension_scores", {}),
            "rubric_scores": parsed.get("rubric_scores", {}),
            "rationale": parsed.get("rationale", ""),
            "strengths": parsed.get("strengths", []),
            "weaknesses": parsed.get("weaknesses", []),
            "raw_evaluation": eval_result
        }

    def _build_eval_prompt(
        self,
        test_case: Dict,
        skill_output: str,
        skill_name: str,
        rubric: Dict = None
    ) -> str:
        """Build evaluation prompt with rubric."""
        test_name = test_case.get("name", "Unknown Test")
        test_description = test_case.get("description", "")
        expected_outputs = test_case.get("expected_outputs", [])
        input_data = test_case.get("input", {})

        # Build expected outputs checklist
        checklist = "\n".join([f"  - {item}" for item in expected_outputs])

        # Custom rubric or default
        if rubric:
            rubric_text = json.dumps(rubric, indent=2)
        else:
            rubric_text = """{
  "accuracy": "Output is factually accurate and relevant to the task",
  "completeness": "Output covers all required aspects comprehensively",
  "actionability": "Recommendations are specific and can be implemented",
  "structure": "Output is well-organized and easy to follow",
  "depth": "Analysis shows deep understanding, not surface-level"
}"""

        return f"""# Role: Independent LLM Judge

You are an expert evaluator assessing AI skill outputs against defined criteria.
Be objective, rigorous, and provide detailed rationale for your scores.

# Task Context
**Test Name:** {test_name}
**Test Description:** {test_description}
**Skill Being Evaluated:** {skill_name}

# Test Input
```
{json.dumps(input_data, indent=2)[:500]}
```

# Expected Outputs (Checklist)
{checklist}

# Skill Output to Evaluate
```
{skill_output[:10000]}  # Truncate for token limits
```

# Evaluation Rubric
{rubric_text}

# Scoring Scale
- 1-2: Poor - Missing critical elements, inaccurate, or irrelevant
- 3-4: Fair - Partial coverage, some useful content but significant gaps
- 5-6: Good - Meets basic requirements, adequate coverage
- 7-8: Very Good - Exceeds requirements, strong analysis
- 9-10: Excellent - Outstanding, comprehensive, actionable insights

# Output Format
Respond with valid JSON only:
```json
{{
  "overall_score": <number 1-10>,
  "dimension_scores": {{
    "accuracy": <number 1-10>,
    "completeness": <number 1-10>,
    "actionability": <number 1-10>,
    "structure": <number 1-10>,
    "depth": <number 1-10>
  }},
  "rubric_scores": {{
    "<rubric_item>": <score and rationale>
  }},
  "rationale": "<2-3 sentence summary of evaluation>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>"]
}}
```

Evaluate objectively. Provide specific examples from the output to support your scores.
"""

    def _invoke_llm(self, prompt: str) -> str:
        """Invoke LLM for evaluation."""
        import requests

        if self.provider == "anthropic":
            return self._invoke_anthropic(prompt)
        elif self.provider == "openai":
            return self._invoke_openai(prompt)
        elif self.provider == "google":
            return self._invoke_google(prompt)
        else:
            return self._invoke_anthropic(prompt)

    def _invoke_google(self, prompt: str) -> str:
        """Invoke Google Vertex AI for evaluation."""
        import requests
        from pathlib import Path
        import google.auth
        import google.auth.transport.urllib3 as google_urllib3
        import urllib3

        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "gcp-auth.json")
        if not os.path.isabs(creds_path):
            project_root = Path(__file__).parent.parent.parent.parent
            creds_path = str(project_root / creds_path)
        creds, _ = google.auth.load_credentials_from_file(
            creds_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        # Refresh token - prefer direct connection, fallback to proxy if env vars set
        proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or ""
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        import google.auth.transport.requests as google_requests
        auth_req_direct = google_requests.Request()
        try:
            creds.refresh(auth_req_direct)
        except Exception:
            if proxy_url:
                _http = urllib3.ProxyManager(proxy_url, cert_reqs="CERT_NONE")
                auth_req = google_urllib3.Request(_http)
                creds.refresh(auth_req)
            else:
                raise

        project_id = creds.project_id if creds.project_id else os.environ.get("GOOGLE_PROJECT_ID", "")
        vertex_url = (
            f"https://us-central1-aiplatform.googleapis.com/v1/"
            f"projects/{project_id}/locations/us-central1/publishers/google/"
            f"models/{self.model}:generateContent"
        )
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 2048, "temperature": 0.3}
        }
        _proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else {}
        # Retry up to 3 times on network/SSL errors (short timeout to fail fast on dead proxy)
        for _req_attempt in range(3):
            try:
                response = requests.post(vertex_url, headers=headers, json=payload, timeout=60, proxies=_proxies, verify=False)
                response.raise_for_status()
                break
            except Exception as _req_e:
                if _req_attempt == 2:
                    raise
                import time as _t; _t.sleep(5)
        result = response.json()
        if "candidates" in result and result["candidates"]:
            parts = result["candidates"][0].get("content", {}).get("parts", [{}])
            return parts[0].get("text", "")
        return ""

    def _invoke_anthropic(self, prompt: str) -> str:
        """Invoke Anthropic Claude API."""
        import requests

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("content", [{}])[0].get("text", "")

    def _invoke_openai(self, prompt: str) -> str:
        """Invoke OpenAI API."""
        import requests

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    def _parse_evaluation(self, eval_text: str) -> Dict:
        """Parse LLM evaluation response."""
        import re

        # Try to extract JSON from response
        json_match = re.search(r'```json\s*(.*?)\s*```', eval_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Fallback: try to parse raw JSON
        try:
            # Find first { and last }
            start = eval_text.find('{')
            end = eval_text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(eval_text[start:end])
        except json.JSONDecodeError:
            pass

        # Return default if parsing fails
        return {
            "overall_score": 5.0,
            "dimension_scores": {
                "accuracy": 5.0,
                "completeness": 5.0,
                "actionability": 5.0,
                "structure": 5.0,
                "depth": 5.0
            },
            "rationale": "Evaluation parsing failed",
            "strengths": [],
            "weaknesses": []
        }


def evaluate_skill_output(
    test_case: Dict,
    skill_output: str,
    skill_name: str,
    provider: str = "anthropic",
    model: str = "claude-sonnet-4-20250514"
) -> Dict:
    """
    Convenience function to evaluate a skill's output.

    Args:
        test_case: Test case definition
        skill_output: Output from the skill
        skill_name: Name of the skill
        provider: LLM provider for judge
        model: Model for judge

    Returns:
        Evaluation result dictionary
    """
    judge = LLMJudge(provider=provider, model=model)
    return judge.evaluate(test_case, skill_output, skill_name)
