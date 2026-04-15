#!/usr/bin/env python3
"""
Benchmark Runner Module

Executes test cases against skills and collects results.
Supports parallel execution, LLM invocation, and LLM Judge evaluation.
"""

import json
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import LLM modules (optional - falls back to simulation if not available)
try:
    from llm_invoker import SkillInvoker, invoke_skill_for_test
    from llm_judge import LLMJudge, evaluate_skill_output
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("  Note: LLM modules not available, using simulated execution")


def run_benchmarks(cluster: Dict, test_suites_dir: Path, parallel: bool = True,
                   max_workers: int = 4, use_llm: bool = False,
                   llm_provider: str = "anthropic") -> List[Dict]:
    """
    Run benchmark tests for all skills in a cluster.

    Args:
        cluster: Cluster data with skills list
        test_suites_dir: Directory containing test suite YAML files
        parallel: Whether to run tests in parallel
        max_workers: Maximum number of parallel workers
        use_llm: Whether to use actual LLM invocation
        llm_provider: LLM provider name

    Returns:
        List of test results for each skill
    """
    cluster_name = cluster["name"]
    cluster_id = cluster["id"]

    # Load test suite
    test_suite_path = test_suites_dir / cluster_name / "tests.yaml"
    if not test_suite_path.exists():
        print(f"   Warning: No test suite found for {cluster_name}")
        return []

    with open(test_suite_path, 'r', encoding='utf-8') as f:
        test_suite = yaml.safe_load(f)

    test_cases = test_suite.get("test_cases", [])

    results = []
    skills = cluster.get("skills", [])

    exec_mode = "LLM" if use_llm else "simulated"
    print(f"   Running {len(test_cases)} tests against {len(skills)} skills ({exec_mode} mode)...")

    if parallel:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_skill = {
                executor.submit(evaluate_skill, skill, test_cases, cluster_name,
                               use_llm=use_llm, llm_provider=llm_provider): skill
                for skill in skills
            }

            for future in as_completed(future_to_skill):
                skill = future_to_skill[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"   Error evaluating {skill.get('name', 'unknown')}: {e}")
    else:
        # Sequential execution
        for skill in skills:
            result = evaluate_skill(skill, test_cases, cluster_name,
                                   use_llm=use_llm, llm_provider=llm_provider)
            results.append(result)

    return results


def evaluate_skill(skill: Dict, test_cases: List[Dict], cluster_name: str,
                   use_llm: bool = False, llm_provider: str = "anthropic") -> Dict:
    """
    Evaluate a single skill against all test cases.

    Args:
        skill: Skill metadata
        test_cases: List of test cases
        cluster_name: Name of the cluster
        use_llm: Whether to use actual LLM invocation
        llm_provider: LLM provider name

    Returns:
        Evaluation result dictionary
    """
    skill_id = skill.get("id", "")
    skill_name = skill.get("name", "")
    skill_path = skill.get("path", "")

    # Initialize LLM components if requested
    skill_invoker = None
    llm_judge = None

    if use_llm and LLM_AVAILABLE:
        skill_invoker = SkillInvoker(provider=llm_provider)
        llm_judge = LLMJudge(provider=llm_provider)

    result = {
        "cluster_name": cluster_name,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "test_results": [],
        "metrics": {
            "total_response_time_s": 0,
            "avg_response_time_s": 0,
            "total_tokens_used": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "success_rate": 0.0,
            "avg_quality_score": 0.0
        },
        "evaluated_at": datetime.now().isoformat(),
        "use_llm": use_llm
    }

    # Try to load skill content for evaluation
    project_root = Path(__file__).parent.parent.parent.parent
    skill_file_path = project_root / skill_path.lstrip("./")

    # 如果路径是目录，尝试查找 SKILL.md
    if skill_file_path.is_dir():
        skill_md = skill_file_path / "SKILL.md"
        if skill_md.exists():
            skill_file_path = skill_md
        else:
            # 跳过没有 SKILL.md 的目录
            return {
                "cluster_name": cluster_name,
                "skill_id": skill_id,
                "skill_name": skill_name,
                "error": "SKILL.md not found",
                "test_results": []
            }

    skill_content = ""
    if skill_file_path.exists() and skill_file_path.is_file():
        skill_content = skill_file_path.read_text(encoding='utf-8')

    # Execute each test case
    for test_case in test_cases:
        try:
            test_result = execute_single_test(
                test_case, skill, skill_content,
                skill_invoker=skill_invoker, llm_judge=llm_judge
            )
        except Exception as _e:
            test_result = {
                "test_id": test_case.get("id", "unknown"),
                "test_name": test_case.get("name", ""),
                "executed": True,
                "response_time_s": 0,
                "tokens_used": 0,
                "success": False,
                "output": f"Error: {_e}",
                "quality_score": 0,
                "dimension_scores": {}
            }
        result["test_results"].append(test_result)

        if test_result.get("success", False):
            result["metrics"]["tests_passed"] += 1
        else:
            result["metrics"]["tests_failed"] += 1

        result["metrics"]["total_response_time_s"] += test_result.get("response_time_s", 0)
        result["metrics"]["total_tokens_used"] += test_result.get("tokens_used", 0)

    # Calculate averages
    num_tests = len(test_cases)
    if num_tests > 0:
        result["metrics"]["avg_response_time_s"] = (
            result["metrics"]["total_response_time_s"] / num_tests
        )
        result["metrics"]["success_rate"] = (
            result["metrics"]["tests_passed"] / num_tests
        )
        # Calculate average quality score
        quality_scores = [tr.get("quality_score", 0) for tr in result["test_results"]]
        result["metrics"]["avg_quality_score"] = sum(quality_scores) / len(quality_scores)

    return result


def execute_single_test(test_case: Dict, skill: Dict, skill_content: str,
                        skill_invoker: SkillInvoker = None, llm_judge: LLMJudge = None) -> Dict:
    """
    Execute a single test case against a skill.

    In production with LLM:
    1. Invoke the skill via LLM API
    2. Measure response time and token usage
    3. Evaluate output quality using LLM Judge
    4. Return detailed results
    """
    start_time = time.time()

    test_input = test_case.get("input", {})
    input_type = test_input.get("type", "text")
    input_value = test_input.get("value", "")

    # Use LLM invoker if available, otherwise simulate
    if skill_invoker and LLM_AVAILABLE:
        result = skill_invoker.invoke_skill(skill, test_input, skill_content)
        output = result.get("output", "")
        response_time = result.get("response_time_s", time.time() - start_time)
        tokens_used = result.get("tokens_used", 0)
        success = result.get("success", False)

        # Use LLM Judge for quality evaluation if available
        if llm_judge and success:
            try:
                eval_result = llm_judge.evaluate(test_case, output, skill.get("name", ""))
                quality_score = eval_result.get("overall_score", 5.0)
                dimension_scores = eval_result.get("dimension_scores", {})
            except Exception as _je:
                quality_score = evaluate_output_quality(output, test_case, skill_content)
                dimension_scores = {}
        else:
            quality_score = evaluate_output_quality(output, test_case, skill_content)
            dimension_scores = {}
    else:
        # Simulate execution
        output = simulate_skill_response(skill, test_case, skill_content)
        response_time = time.time() - start_time
        tokens_used = len(output) // 4
        success = True
        quality_score = evaluate_output_quality(output, test_case, skill_content)
        dimension_scores = {}

    return {
        "test_id": test_case.get("id", "unknown"),
        "test_name": test_case.get("name", ""),
        "executed": True,
        "response_time_s": round(response_time, 3),
        "tokens_used": tokens_used,
        "success": success,
        "output": output[:500],  # Truncate for storage
        "quality_score": quality_score,
        "dimension_scores": dimension_scores,
        "scoring_breakdown": {
            "speed": calculate_speed_score(response_time, test_case),
            "quality": quality_score * 5,  # Normalize to 50 points
            "maintainability": evaluate_maintainability(output, test_case)
        }
    }


def simulate_skill_response(skill: Dict, test_case: Dict, skill_content: str) -> str:
    """
    Simulate skill response for testing with realistic variations.

    Different skills produce different quality outputs based on their metadata.
    """
    skill_id = skill.get("id", "")
    skill_name = skill.get("name", "Unknown Skill")
    skill_version = skill.get("version", "1.0.0")
    test_name = test_case.get("name", "Unknown Test")

    # Generate deterministic but varied quality score based on skill ID
    # This simulates that some skills are genuinely better than others
    quality_seed = hash(skill_id) % 100

    # Top performers (seed >= 80): comprehensive, well-structured responses
    if quality_seed >= 80:
        quality_tier = "excellent"
        response = f"""# {test_name} - Analysis Report

## Executive Summary

This is a comprehensive analysis provided by **{skill_name}** (v{skill_version}).

## Detailed Analysis

### Key Findings

1. **Primary Insight**: Deep analysis reveals critical patterns
2. **Secondary Insight**: Supporting evidence from multiple angles
3. **Recommendation**: Actionable next steps with implementation details

### Methodology

Our analysis follows industry best practices:
- Data-driven approach with statistical validation
- Cross-referenced with industry benchmarks
- Risk assessment and mitigation strategies

## Recommendations

### Immediate Actions (Week 1)
- Prioritize high-impact items first
- Quick wins for momentum

### Short-term (Month 1)
- Systematic implementation of core improvements
- Team training and alignment

### Long-term (Quarter 1)
- Sustainable process improvements
- Continuous monitoring framework

## Conclusion

This analysis provides a roadmap for success with measurable outcomes.

---
*Generated by {skill_name}*
"""
    # Good performers (seed 50-79): solid but less comprehensive
    elif quality_seed >= 50:
        quality_tier = "good"
        response = f"""# {test_name} Analysis

## Overview

Analysis by {skill_name} (v{skill_version}).

## Key Points

1. Important finding with supporting details
2. Secondary observation with context
3. Recommendation for improvement

## Implementation Steps

1. Start with assessment
2. Prioritize based on impact
3. Execute in phases
4. Monitor and adjust

## Summary

Solid recommendations for moving forward.

---
*{skill_name}*
"""
    # Average performers (seed 20-49): basic coverage
    else:
        quality_tier = "basic"
        response = f"""Analysis by {skill_name}

Key observations:
- Point 1 about the topic
- Point 2 with some detail
- Recommendation to consider

Basic framework for implementation.

More details can be added as needed.

---
{skill_name}
"""

    return response


def evaluate_output_quality(output: str, test_case: Dict, skill_content: str) -> float:
    """
    Evaluate output quality against expected outputs and rubric.

    Returns a score from 0.0 to 10.0 based on:
    - Coverage of expected outputs
    - Structure and formatting
    - Depth and actionability
    """
    score = 0.0

    # Get expected outputs from test case
    expected_outputs = test_case.get("expected_outputs", [])
    output_lower = output.lower()

    # Score based on coverage of expected outputs (up to 5 points)
    if expected_outputs:
        matched = 0
        for expected in expected_outputs:
            # Check if expected content is present (fuzzy match)
            expected_lower = expected.lower()
            # Extract key terms from expected output
            key_terms = [w for w in expected_lower.split() if len(w) > 4 and w not in ['would', 'should', 'could', 'output', 'expected']]
            matches_term = any(term in output_lower for term in key_terms[:3])  # Check first 3 terms
            if matches_term or expected_lower[:20] in output_lower:
                matched += 1

        coverage_ratio = matched / len(expected_outputs)
        score += coverage_ratio * 5.0
    else:
        # Fallback heuristics when no expected outputs defined
        score += 2.5  # Base score

    # Structure and formatting (up to 2 points)
    structure_indicators = ["##", "**", "1.", "- ", "conclusion", "summary", "recommendation"]
    structure_count = sum(1 for indicator in structure_indicators if indicator in output_lower)
    score += min(2.0, structure_count * 0.25)

    # Depth indicators (up to 2 points)
    depth_indicators = ["analysis", "detailed", "comprehensive", "framework", "methodology",
                        "implementation", "strategy", "roadmap", "prioritize", "impact"]
    depth_count = sum(1 for indicator in depth_indicators if indicator in output_lower)
    score += min(2.0, depth_count * 0.2)

    # Length bonus (up to 1 point) - longer is often better
    if len(output) > 300:
        score += 0.25
    if len(output) > 600:
        score += 0.25
    if len(output) > 1000:
        score += 0.5

    return min(10.0, score)


def calculate_speed_score(response_time: float, test_case: Dict) -> float:
    """Calculate speed score (0-30 points)."""
    # Get threshold from test case or use default
    scoring = test_case.get("scoring", {})
    speed_config = scoring.get("speed", {})
    threshold = speed_config.get("threshold_s", 10)

    if response_time < threshold * 0.5:
        return 30.0  # Full points
    elif response_time < threshold:
        return 30.0 * (1 - (response_time - threshold * 0.5) / threshold * 2)
    else:
        return max(0, 30.0 * (threshold / response_time) * 0.5)


def evaluate_maintainability(output: str, test_case: Dict) -> float:
    """
    Evaluate output maintainability (0-20 points).

    Based on:
    - Structure and organization
    - Clarity and readability
    - Reusability of content
    """
    score = 0.0

    # Structure (0-10 points)
    # Uses markdown headers
    if output.count("##") >= 3:
        score += 3.0
    elif output.count("##") >= 1:
        score += 1.5

    # Uses bold/emphasis
    if output.count("**") >= 4:
        score += 2.0
    elif output.count("**") >= 2:
        score += 1.0

    # Uses lists
    if output.count("- ") >= 3 or output.count("1.") >= 2:
        score += 2.0

    # Has clear sections
    if any(section in output.lower() for section in ["conclusion", "summary", "recommendation"]):
        score += 3.0

    # Clarity (0-10 points)
    # Good line breaks
    if output.count("\n") >= 15:
        score += 3.0
    elif output.count("\n") >= 8:
        score += 1.5

    # Uses code blocks (if applicable)
    if "```" in output:
        score += 2.0

    # Has actionable items
    action_words = ["action", "step", "implement", "execute", "prioritize", "framework"]
    if any(word in output.lower() for word in action_words):
        score += 3.0

    # Clear formatting throughout
    if len(output) > 200 and output.count("\n") / max(1, len(output)) > 0.05:
        score += 2.0

    return min(20.0, score)


def estimate_tokens(text: str) -> int:
    """Estimate token count from text length."""
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4
