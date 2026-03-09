#!/usr/bin/env python3
"""
Skill Clustering Module

Scans the project for skills and clusters them by semantic similarity.
"""

import json
import hashlib
import os
from pathlib import Path
from typing import List, Dict, Any


def scan_skills(project_root: Path) -> List[Dict[str, Any]]:
    """
    Scan project for all skills.

    Looks in:
    - index.json registered skills
    - community/, engineering/, creative/, productivity/, devops/
    - external/*/ directories
    """
    skills = []

    # Method 1: Scan index.json
    index_path = project_root / "index.json"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)

        for skill in index_data.get("skills", []):
            skills.append({
                "id": skill.get("id", ""),
                "name": skill.get("name", ""),
                "path": skill.get("path", ""),
                "description": skill.get("description", ""),
                "tags": skill.get("tags", []),
                "source": "index.json"
            })

    # Method 2: Scan directories for SKILL.md files
    skill_md_patterns = [
        "community/*/SKILL.md",
        "engineering/*/SKILL.md",
        "creative/*/SKILL.md",
        "productivity/*/SKILL.md",
        "devops/*/SKILL.md",
        "external/*/skills/*/SKILL.md",
        "external/*/*/*/SKILL.md",
    ]

    scanned_ids = set(s["id"] for s in skills)

    for pattern in skill_md_patterns:
        for skill_md in project_root.glob(pattern):
            # Extract skill ID from directory name
            skill_id = skill_md.parent.name.lower().replace('_', '-').replace(' ', '-')

            if skill_id not in scanned_ids:
                scanned_ids.add(skill_id)
                skills.append({
                    "id": skill_id,
                    "name": skill_id,
                    "path": str(skill_md.relative_to(project_root)),
                    "description": "",
                    "tags": [],
                    "source": f"scan:{pattern}"
                })

    return skills


def analyze_skills(skills: List[Dict], project_root: Path) -> List[Dict]:
    """
    Analyze each skill's semantics.

    For each skill:
    1. Read SKILL.md content
    2. Extract key information (name, description, tags)
    3. Generate semantic embedding (using LLM or simple keyword extraction)
    4. Analyze code structure if applicable
    """
    analyzed = []

    for skill in skills:
        analysis = {**skill}

        # Read SKILL.md content
        skill_path = project_root / skill["path"]
        if skill_path.exists():
            content = skill_path.read_text(encoding='utf-8')

            # Extract frontmatter if present
            import re
            frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)

                # Extract name
                name_match = re.search(r'^name:\s*(.+?)$', frontmatter, re.MULTILINE)
                if name_match:
                    analysis["name"] = name_match.group(1).strip()

                # Extract description
                desc_match = re.search(r'^description:\s*(.+?)$', frontmatter, re.MULTILINE)
                if desc_match:
                    analysis["description"] = desc_match.group(1).strip()

                # Extract tags
                tags_match = re.search(r'^tags:\s*\[(.*?)\]', frontmatter, re.MULTILINE)
                if tags_match:
                    analysis["tags"] = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]

            # Generate keyword embedding (simplified - in production use LLM)
            analysis["keywords"] = extract_keywords(analysis)

            # Analyze complexity (simplified)
            analysis["complexity"] = analyze_complexity(content)

        analyzed.append(analysis)

    return analyzed


def extract_keywords(analysis: Dict) -> List[str]:
    """Extract keywords from skill metadata."""
    keywords = []

    # From tags
    keywords.extend(analysis.get("tags", []))

    # From name
    name = analysis.get("name", "").lower()
    keywords.extend(name.replace('-', ' ').replace('_', ' ').split())

    # From description (top words)
    desc = analysis.get("description", "").lower()
    # Simple word extraction (in production use TF-IDF or LLM)
    words = [w for w in desc.split() if len(w) > 3 and w not in STOPWORDS]
    keywords.extend(words[:10])

    return list(set(keywords))


def analyze_complexity(content: str) -> str:
    """Analyze skill complexity based on content length and structure."""
    lines = content.count('\n')
    sections = content.count('##')

    if lines > 500 or sections > 10:
        return "expert"
    elif lines > 200 or sections > 5:
        return "advanced"
    elif lines > 100 or sections > 3:
        return "intermediate"
    else:
        return "beginner"


def cluster_skills(analyzed_skills: List[Dict]) -> List[Dict]:
    """
    Cluster skills by semantic similarity.

    Uses a combination of:
    1. Keyword overlap
    2. Tag similarity
    3. LLM-based semantic analysis (in production)

    Returns clusters with skills grouped by functionality.
    """
    # Predefined category mapping (simplified clustering)
    # In production, use hierarchical clustering or LLM-based classification

    category_keywords = {
        "cro": ["cro", "conversion", "optimization", "landing", "signup", "form", "popup", "paywall", "onboarding"],
        "seo": ["seo", "search", "ranking", "schema", "markup", "audit", "ai-seo", "programmatic"],
        "content": ["content", "copywriting", "copy", "editing", "social", "email", "sequence"],
        "marketing": ["marketing", "ads", "paid", "campaign", "analytics", "tracking", "ab-test"],
        "growth": ["growth", "referral", "churn", "retention", "viral"],
        "sales": ["sales", "cold", "outreach", "enablement", "revops"],
        "pricing": ["pricing", "pricing-strategy", "monetization"],
        "engineering": ["engineering", "code", "development", "git", "testing", "debugging"],
        "product": ["product", "ux", "design", "frontend"],
        "devops": ["devops", "deployment", "ci-cd", "infrastructure", "mcp"],
        "data": ["data", "analytics", "spreadsheet", "xlsx", "pdf"],
        "video": ["video", "media", "image", "photo"],
        "agent": ["agent", "context", "memory", "multi-agent", "tool"],
        "creative": ["creative", "design", "art", "visual"],
        "business": ["business", "finance", "c-level", "advisor"],
        "compliance": ["compliance", "ra-qm", "iso", "gdpr", "fda", "regulatory"],
    }

    # Assign skills to categories
    clusters = {cat: [] for cat in category_keywords.keys()}
    unassigned = []

    for skill in analyzed_skills:
        keywords = skill.get("keywords", [])
        name = skill.get("name", "").lower()
        skill_id = skill.get("id", "")

        best_match = None
        best_score = 0

        for category, cat_keywords in category_keywords.items():
            score = sum(1 for kw in cat_keywords if kw in name or kw in keywords)
            if score > best_score:
                best_score = score
                best_match = category

        if best_match and best_score > 0:
            clusters[best_match].append(skill)
        else:
            unassigned.append(skill)

    # Create cluster objects
    result = []
    for category, skills in clusters.items():
        if skills:
            result.append({
                "id": f"cluster-{len(result)+1:03d}-{category}",
                "name": category,
                "description": f"{category.title()} skills",
                "skills": skills,
                "skill_count": len(skills)
            })

    # Handle unassigned skills
    if unassigned:
        result.append({
            "id": f"cluster-{len(result)+1:03d}-other",
            "name": "other",
            "description": "Other uncategorized skills",
            "skills": unassigned,
            "skill_count": len(unassigned)
        })

    return result


STOPWORDS = {
    'this', 'that', 'with', 'for', 'from', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
    'now', 'about', 'over', 'any', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'would', 'could', 'should', 'may', 'might',
    'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'to', 'of',
    'in', 'and', 'or', 'but', 'if', 'while', 'although', 'though', 'after',
    'before', 'because', 'since', 'until', 'unless', 'whether', 'what',
    'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'user',
    'use', 'useful', 'used', 'using', 'skill', 'skills', 'use when',
}
