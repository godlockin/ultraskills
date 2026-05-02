#!/usr/bin/env python3
"""
Expert Collaboration Module

Orchestrates collaboration between domain experts to design comprehensive test cases.
Simulates a roundtable discussion where each expert contributes their perspective.
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from expert_panels import get_expert_panel, format_expert_panel_for_prompt

try:
    from llm_invoker import SkillInvoker
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False


def summon_experts(cluster: Dict, project_context: Dict = None) -> Dict:
    """
    Summon expert panel for a category and prepare collaboration context.

    This function sets up the expert panel with full context about:
    - The skills being tested
    - The category domain
    - Project-specific constraints
    - Test design requirements
    """
    category = cluster.get("name", "other")
    panel = get_expert_panel(category)

    # Prepare skills context
    skills_context = []
    for skill in cluster.get("skills", []):
        skills_context.append({
            "id": skill.get("id", ""),
            "name": skill.get("name", ""),
            "description": skill.get("description", ""),
            "tags": skill.get("tags", [])
        })

    return {
        "panel": panel,
        "category": category,
        "skills": skills_context,
        "project_context": project_context or {},
        "task": "design_test_cases"
    }


def run_expert_roundtable(context: Dict) -> List[Dict]:
    """
    Simulate expert roundtable discussion for test case design.

    Each expert contributes from their perspective:
    1. Opening statements - understanding of the task
    2. Individual contributions - specific test ideas from their expertise
    3. Cross-examination - critiquing and building on each other's ideas
    4. Consensus building - agreeing on final test case set
    """
    panel = context["panel"]
    category = context["category"]
    skills = context["skills"]

    # Round 1: Opening statements
    opening_statements = []
    for expert in panel["experts"]:
        statement = generate_expert_opening(expert, category, skills)
        opening_statements.append({
            "expert": expert["name"],
            "statement": statement
        })

    # Round 2: Individual test case proposals
    test_proposals = []
    for expert in panel["experts"]:
        proposals = generate_expert_test_proposals(expert, category, skills)
        test_proposals.extend(proposals)

    # Round 3: Cross-examination and refinement
    refined_tests = refine_tests_collaborative(test_proposals, panel, category)

    # Round 4: Consensus on final test suite
    final_tests = build_consensus_test_suite(refined_tests, panel, category)

    return final_tests


def generate_expert_opening(expert: Dict, category: str, skills: List) -> str:
    """Generate opening statement from an expert's perspective."""
    # This is a simplified version - in production, use LLM to generate
    focus_areas = expert.get("focus", "")
    expertise = expert.get("expertise", [])

    return f"""As {expert['title']}, my focus for this {category} test suite is on {focus_areas}.
I'll ensure we cover: {', '.join(expertise[:2])}.
Key consideration: We need tests that evaluate both theoretical knowledge and practical application."""


def generate_expert_test_proposals(expert: Dict, category: str, skills: List) -> List[Dict]:
    """Generate test case proposals from an expert's perspective."""
    # Template test proposals based on expert focus
    proposals = []
    base_id = len(proposals) + 1

    # Each expert proposes 2-3 tests from their perspective
    proposal_templates = generate_test_proposals_with_llm(category, skills)

    for template in proposal_templates[:3]:
        proposals.append({
            "id": f"tc-{base_id:03d}",
            "name": template["name"],
            "description": template["description"],
            "input": template["input"],
            "expected_outputs": template["expected_outputs"],
            "scoring": template["scoring"],
            "proposed_by": expert["name"],
            "expert_focus": expert["focus"]
        })
        base_id += 1

    return proposals


def generate_test_proposals_with_llm(category: str, skills_context: List[Dict]) -> List[Dict]:
    """
    Generate meaningful test proposals using LLM based on real skill descriptions.
    Falls back to hardcoded templates if LLM unavailable or call fails.
    """
    if not _LLM_AVAILABLE:
        return get_proposal_templates_for_category(category)

    # Check if we have hardcoded templates for this category
    hardcoded = _HARDCODED_TEMPLATES.get(category)
    if hardcoded:
        return hardcoded

    # Build skills description for prompt
    skills_desc_lines = []
    for s in skills_context[:10]:  # cap at 10 to avoid huge prompts
        desc = s.get("description", "").strip()
        name = s.get("name") or s.get("id", "")
        tags = ", ".join(s.get("tags", []))
        skills_desc_lines.append(f"- {name}: {desc}" + (f" [tags: {tags}]" if tags else ""))
    skills_descriptions = "\n".join(skills_desc_lines) or f"Skills in the {category} category"

    prompt = f"""Design 3 benchmark test cases for AI skills in the "{category}" category.

Skills to test:
{skills_descriptions}

Return a flat JSON array. Each element must have these fields (ALL values are single-line strings, NO newlines inside values):
- name: short test name
- description: what this test evaluates
- input_type: one of: text, code, scenario, architecture
- input_value: a specific realistic input (single line, no newlines)
- criterion_1: first evaluation criterion
- criterion_2: second evaluation criterion
- criterion_3: third evaluation criterion

Return ONLY the JSON array. No markdown fences. No newlines inside string values."""

    try:
        invoker = SkillInvoker(provider="google", model="gemini-2.5-flash")
        result = invoker.invoke_skill(
            skill={"id": "test-designer", "name": "Test Case Designer"},
            test_input={"type": "text", "value": prompt},
            skill_content=""
        )
        if not result.get("success"):
            raise RuntimeError(result.get("error", "LLM call failed"))

        content = result.get("output", "")
        # Strip markdown code fences if present
        content = re.sub(r"^```(?:json)?\s*", "", content.strip())
        content = re.sub(r"\s*```$", "", content.strip())
        # Strip markdown fences and extract JSON array
        _match = re.search(r'\[.*\]', content, re.DOTALL)
        if _match:
            content = _match.group(0)
        # Try strict parse first, then repair trailing commas
        try:
            flat_proposals = json.loads(content)
        except json.JSONDecodeError:
            content_fixed = re.sub(r',\s*([}\]])', r'\1', content)
            flat_proposals = json.loads(content_fixed)
        if not isinstance(flat_proposals, list) or len(flat_proposals) == 0:
            raise ValueError("Empty or non-list LLM response")
        # Convert flat schema to expected nested format
        proposals = []
        for item in flat_proposals:
            if not isinstance(item, dict):
                continue
            proposals.append({
                "name": item.get("name", "Test Case"),
                "description": item.get("description", ""),
                "input": {
                    "type": item.get("input_type", "text"),
                    "value": item.get("input_value", item.get("value", ""))
                },
                "expected_outputs": [
                    item.get("criterion_1", ""),
                    item.get("criterion_2", ""),
                    item.get("criterion_3", ""),
                ],
                "scoring": {
                    "speed": {"weight": 0.3, "max_points": 30},
                    "quality": {"weight": 0.5, "max_points": 50},
                    "maintainability": {"weight": 0.2, "max_points": 20}
                }
            })
        if proposals:
            return proposals
        raise ValueError("No valid proposals after conversion")

    except Exception as e:
        # Fallback to default template
        print(f"[expert_collaboration] LLM test generation failed for '{category}': {e}. Using fallback.")
        return get_proposal_templates_for_category(category)


# Internal: hardcoded templates used by get_proposal_templates_for_category
_HARDCODED_TEMPLATES = {
    "cro": [
        {
            "name": "Landing Page Conversion Audit",
            "description": "Analyze a landing page and identify conversion barriers",
            "input": {"type": "url", "value": "https://example.com/landing"},
            "expected_outputs": [
                "Identify 3+ conversion barriers",
                "Provide prioritized recommendations",
                "Include implementation guidance"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        },
        {
            "name": "A/B Test Design Challenge",
            "description": "Design an A/B test for a given conversion problem",
            "input": {"type": "scenario", "value": "Problem: 70% cart abandonment"},
            "expected_outputs": [
                "Clear hypothesis",
                "Test variant description",
                "Success metrics",
                "Sample size calculation"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        },
        {
            "name": "Copy Optimization Challenge",
            "description": "Rewrite weak copy to improve conversions",
            "input": {"type": "copy", "value": "Weak headline and CTA provided"},
            "expected_outputs": [
                "Critique of original copy",
                "3 alternative versions",
                "Rationale for each version"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        }
    ],
    "seo": [
        {
            "name": "Technical SEO Audit",
            "description": "Perform comprehensive technical SEO audit",
            "input": {"type": "url", "value": "https://example.com"},
            "expected_outputs": [
                "Identify critical technical issues",
                "Prioritize by impact",
                "Provide fix instructions"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        },
        {
            "name": "Content Optimization for AI Search",
            "description": "Optimize content for AI Overview visibility",
            "input": {"type": "content", "value": "Article content provided"},
            "expected_outputs": [
                "AI search optimization recommendations",
                "Structured data suggestions",
                "Entity optimization ideas"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        }
    ],
    "engineering": [
        {
            "name": "Code Review Challenge",
            "description": "Review code for bugs, security issues, and quality",
            "input": {"type": "code", "value": "Sample code snippet provided"},
            "expected_outputs": [
                "Identify bugs and security issues",
                "Suggest refactoring improvements",
                "Evaluate code style and patterns"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        },
        {
            "name": "Architecture Design Review",
            "description": "Evaluate system architecture and provide recommendations",
            "input": {"type": "architecture", "value": "System design document"},
            "expected_outputs": [
                "Identify architectural risks",
                "Suggest improvements",
                "Evaluate scalability and maintainability"
            ],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        }
    ]
}


def get_proposal_templates_for_category(category: str) -> List[Dict]:
    """Get test proposal templates by category. Uses hardcoded set for known categories, generic default otherwise."""
    default = [
        {
            "name": f"Standard {category.title()} Task",
            "description": f"Evaluate skill performance on typical {category} task",
            "input": {"type": "text", "value": f"Test input for {category}"},
            "expected_outputs": ["Relevant and accurate output"],
            "scoring": {
                "speed": {"weight": 0.3, "max_points": 30},
                "quality": {"weight": 0.5, "max_points": 50},
                "maintainability": {"weight": 0.2, "max_points": 20}
            }
        }
    ]
    return _HARDCODED_TEMPLATES.get(category, default)


def refine_tests_collaborative(proposals: List[Dict], panel: Dict, category: str) -> List[Dict]:
    """
    Refine test proposals through expert cross-examination.

    Process:
    1. Identify duplicate/overlapping tests
    2. Merge similar tests
    3. Fill gaps identified by experts
    4. Ensure comprehensive coverage
    """
    # Simplified refinement - in production use LLM for actual collaboration
    refined = []
    seen_names = set()

    for proposal in proposals:
        name_key = proposal["name"].lower()
        if name_key not in seen_names:
            seen_names.add(name_key)
            # Add refinement notes
            proposal["refinement_notes"] = [
                f"Reviewed by {panel['experts'][0]['name']}",
                f"Aligned with {category} best practices"
            ]
            refined.append(proposal)

    return refined


def build_consensus_test_suite(refined_tests: List[Dict], panel: Dict, category: str) -> List[Dict]:
    """
    Build final consensus test suite.

    Select 5-10 tests that:
    1. Cover all major skill dimensions
    2. Include input from all experts
    3. Progress from simple to complex
    4. Are practical to execute
    """
    # Select top tests ensuring coverage
    final_suite = refined_tests[:7]  # Limit to 7 tests for practicality

    # Add consensus notes
    for test in final_suite:
        test["consensus"] = {
            "approved_by": [e["name"] for e in panel["experts"]],
            "category": category,
            "coverage": "comprehensive"
        }

    return final_suite


def design_test_cases_collaborative(cluster: Dict, test_suites_dir: Path) -> Path:
    """
    Main entry point: Design test cases through expert collaboration.

    Workflow:
    1. Summon expert panel
    2. Run roundtable discussion
    3. Generate final test suite
    4. Save to YAML file
    """
    category = cluster["name"]
    cluster_dir = test_suites_dir / category
    cluster_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Summon experts
    context = summon_experts(cluster)

    # Step 2: Run roundtable
    test_cases = run_expert_roundtable(context)

    # Step 3: Build test suite YAML
    test_suite = {
        "cluster": cluster["id"],
        "name": f"{category.title()} Skills Benchmark",
        "version": "1.0.0",
        "description": f"Expert-designed test suite for {category} skills",
        "expert_panel": {
            "name": context["panel"]["panel_name"],
            "experts": [e["name"] for e in context["panel"]["experts"]]
        },
        "test_cases": test_cases
    }

    # Step 4: Save to YAML
    tests_yaml_path = cluster_dir / "tests.yaml"
    with open(tests_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(test_suite, f, allow_unicode=True, default_flow_style=False)

    # Also save expert discussion log
    discussion_log_path = cluster_dir / "expert-discussion.json"
    with open(discussion_log_path, 'w', encoding='utf-8') as f:
        json.dump({
            "context": context,
            "final_tests": test_cases
        }, f, indent=2, ensure_ascii=False)

    return tests_yaml_path
