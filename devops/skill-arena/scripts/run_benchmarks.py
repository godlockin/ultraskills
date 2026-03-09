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

    skill_content = ""
    if skill_file_path.exists():
        skill_content = skill_file_path.read_text(encoding='utf-8')

    # Execute each test case
    for test_case in test_cases:
        test_result = execute_single_test(
            test_case, skill, skill_content,
            skill_invoker=skill_invoker, llm_judge=llm_judge
        )
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
            eval_result = llm_judge.evaluate(test_case, output, skill.get("name", ""))
            quality_score = eval_result.get("overall_score", 5.0)
            dimension_scores = eval_result.get("dimension_scores", {})
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
    Simulate skill response for testing.

    In production, replace with actual LLM invocation.
    """
    skill_name = skill.get("name", "Unknown Skill")
    test_name = test_case.get("name", "Unknown Test")

    return f"""[Simulated Response from {skill_name}]

Test: {test_name}

Analysis:
This is a simulated response for testing purposes. In production, this would
contain the actual skill's analysis and recommendations based on the test input.

Key Points:
1. The skill would analyze the input ({test_case.get('input', {}).get('type', 'text')})
2. Apply domain-specific knowledge
3. Generate actionable recommendations
4. Structure output according to best practices

Quality Indicators:
- Comprehensive coverage of the topic
- Clear, actionable recommendations
- Well-structured output
- Appropriate use of formatting

[End of simulated response]
"""


def evaluate_output_quality(output: str, test_case: Dict, skill_content: str) -> float:
    """
    Evaluate output quality.

    In production, use LLM judge with detailed rubric.
    For now, return simulated score based on output characteristics.
    """
    # Simple heuristics for simulation
    score = 5.0  # Base score

    # Longer, more detailed responses get higher scores
    if len(output) > 500:
        score += 1.0
    if len(output) > 1000:
        score += 1.0

    # Responses that mention key aspects get bonus
    output_lower = output.lower()
    if "analysis" in output_lower:
        score += 0.5
    if "recommendation" in output_lower or "suggestion" in output_lower:
        score += 0.5
    if "key" in output_lower or "important" in output_lower:
        score += 0.5

    # Cap at 10
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
    """Evaluate output maintainability (0-20 points)."""
    score = 10.0  # Base score

    # Well-structured outputs get bonus
    if "##" in output or "**" in output:
        score += 2.0  # Uses markdown formatting
    if output.count("\n") > 10:
        score += 2.0  # Good line breaks
    if "```" in output:
        score += 2.0  # Uses code blocks

    # Check for clear structure
    if any(marker in output.lower() for marker in ["conclusion", "summary", "key points"]):
        score += 2.0

    return min(20.0, score)


def estimate_tokens(text: str) -> int:
    """Estimate token count from text length."""
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4
