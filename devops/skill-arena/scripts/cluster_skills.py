#!/usr/bin/env python3
"""
Skill Clustering Module - Hierarchical Fine-Grained Clustering

Scans the project for skills and clusters them into fine-grained subcategories.
Each subcategory has dedicated expert panel and specialized test cases.
"""

import json
import hashlib
import os
from pathlib import Path
from typing import List, Dict, Any


def scan_skills(project_root: Path) -> List[Dict[str, Any]]:
    """Scan project for all skills."""
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
    """Analyze each skill's semantics."""
    analyzed = []

    for skill in skills:
        analysis = {**skill}
        skill_path = project_root / skill["path"]

        # 如果路径是目录，尝试查找 SKILL.md
        if skill_path.is_dir():
            skill_md = skill_path / "SKILL.md"
            if skill_md.exists():
                skill_path = skill_md
            else:
                continue  # 跳过没有 SKILL.md 的目录

        if skill_path.exists() and skill_path.is_file():
            content = skill_path.read_text(encoding='utf-8')

            # Extract frontmatter
            import re
            frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)

                name_match = re.search(r'^name:\s*(.+?)$', frontmatter, re.MULTILINE)
                if name_match:
                    analysis["name"] = name_match.group(1).strip()

                desc_match = re.search(r'^description:\s*(.+?)$', frontmatter, re.MULTILINE)
                if desc_match:
                    analysis["description"] = desc_match.group(1).strip()

                tags_match = re.search(r'^tags:\s*\[(.*?)\]', frontmatter, re.MULTILINE)
                if tags_match:
                    analysis["tags"] = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]

            analysis["keywords"] = extract_keywords(analysis)
            analysis["complexity"] = analyze_complexity(content)
            analysis["content_length"] = len(content)
            analysis["section_count"] = content.count('##')

        analyzed.append(analysis)

    return analyzed


def extract_keywords(analysis: Dict) -> List[str]:
    """Extract keywords from skill metadata."""
    keywords = []

    keywords.extend(analysis.get("tags", []))

    name = analysis.get("name", "").lower()
    keywords.extend(name.replace('-', ' ').replace('_', ' ').split())

    desc = analysis.get("description", "").lower()
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
    Cluster skills into fine-grained subcategories.

    Hierarchy:
    - Category (e.g., Engineering)
      - Subcategory (e.g., Code Quality, Testing, Architecture, DevOps, Security)
        - Skills
    """

    # Fine-grained subcategory mapping with specific keywords
    subcategories = {
        # Engineering subcategories
        "eng-code-quality": {
            "parent": "engineering",
            "keywords": ["code-review", "review", "quality", "refactor", "clean-code", "lint"],
            "experts": ["Martin Fowler", "Kent Beck"],
            "test_focus": "code analysis, bug detection, best practices"
        },
        "eng-testing": {
            "parent": "engineering",
            "keywords": ["testing", "tdd", "test", "pytest", "webapp-testing", "playwright"],
            "experts": ["Kent Beck", "Jessica Kerr"],
            "test_focus": "test strategy, coverage, edge cases"
        },
        "eng-architecture": {
            "parent": "engineering",
            "keywords": ["architecture", "design", "system-design", "scalability", "microservices"],
            "experts": ["Martin Fowler", "Will Larson"],
            "test_focus": "system design, trade-offs, scalability"
        },
        "eng-devops": {
            "parent": "engineering",
            "keywords": ["devops", "ci-cd", "deployment", "pipeline", "git-worktree", "release", "skill-manager", "skill-sync", "planning", "file-based", "task-plan"],
            "experts": ["Kelsey Hightower", "Charity Majors"],
            "test_focus": "CI/CD, deployment, monitoring, skill lifecycle management"
        },
        "eng-security": {
            "parent": "engineering",
            "keywords": ["security", "auth", "secret", "vulnerability", "owasp"],
            "experts": ["Will Larson", "Jez Humble"],
            "test_focus": "security review, vulnerability detection"
        },

        # SEO subcategories
        "seo-technical": {
            "parent": "seo",
            "keywords": ["technical-seo", "schema", "markup", "core-web-vitals", "crawl"],
            "experts": ["Dr. Michael Brenner", "Ahmed Hassan"],
            "test_focus": "technical audit, schema markup"
        },
        "seo-content": {
            "parent": "seo",
            "keywords": ["content-seo", "ai-seo", "keyword", "optimization", "programmatic"],
            "experts": ["Lisa Chang", "Rachel Green"],
            "test_focus": "content optimization, keyword strategy"
        },
        "seo-local": {
            "parent": "seo",
            "keywords": ["local-seo", "gmb", "citation", "local-pack"],
            "experts": ["Dr. Michael Brenner"],
            "test_focus": "local optimization, GBP"
        },

        # CRO subcategories
        "cro-landing": {
            "parent": "cro",
            "keywords": ["landing", "page-cro", "page", "conversion"],
            "experts": ["Dr. Sarah Chen", "Marcus Rodriguez"],
            "test_focus": "landing page analysis, conversion barriers"
        },
        "cro-form": {
            "parent": "cro",
            "keywords": ["form", "signup", "checkout", "input"],
            "experts": ["Marcus Rodriguez", "James Park"],
            "test_focus": "form optimization, friction analysis"
        },
        "cro-funnel": {
            "parent": "cro",
            "keywords": ["funnel", "onboarding", "paywall", "popup"],
            "experts": ["Dr. Emily Watson", "James Park"],
            "test_focus": "funnel analysis, drop-off points"
        },
        "cro-ab-testing": {
            "parent": "cro",
            "keywords": ["ab-test", "experiment", "personalization", "heatmap"],
            "experts": ["Dr. Sarah Chen", "James Park"],
            "test_focus": "A/B test design, statistical analysis"
        },

        # Content subcategories
        "content-copywriting": {
            "parent": "content",
            "keywords": ["copywriting", "copy", "headline", "cta"],
            "experts": ["David Ogilvy Jr.", "Ann Handley"],
            "test_focus": "copy analysis, persuasion"
        },
        "content-strategy": {
            "parent": "content",
            "keywords": ["content-strategy", "planning", "editorial"],
            "experts": ["Ann Handley"],
            "test_focus": "content planning, strategy"
        },
        "content-social": {
            "parent": "content",
            "keywords": ["social", "twitter", "linkedin", "engagement"],
            "experts": ["Mari Smith"],
            "test_focus": "social media strategy"
        },
        "content-email": {
            "parent": "content",
            "keywords": ["email", "sequence", "newsletter"],
            "experts": ["Ann Handley"],
            "test_focus": "email copy, sequences"
        },

        # Marketing subcategories
        "marketing-analytics": {
            "parent": "marketing",
            "keywords": ["analytics", "tracking", "measurement", "attribution"],
            "experts": ["Avinash Kaushik"],
            "test_focus": "analytics setup, attribution"
        },
        "marketing-paid": {
            "parent": "marketing",
            "keywords": ["paid", "ads", "ppc", "campaign"],
            "experts": ["Neil Patel"],
            "test_focus": "ad strategy, ROI"
        },
        "marketing-growth": {
            "parent": "marketing",
            "keywords": ["growth", "viral", "referral", "free-tool"],
            "experts": ["Rand Fishkin"],
            "test_focus": "growth loops, viral mechanics"
        },

        # Product subcategories
        "product-strategy": {
            "parent": "product",
            "keywords": ["product-strategy", "roadmap", "vision"],
            "experts": ["Marty Cagan"],
            "test_focus": "product vision, strategy"
        },
        "product-discovery": {
            "parent": "product",
            "keywords": ["discovery", "research", "interview", "user"],
            "experts": ["Teresa Torres", "Don Norman"],
            "test_focus": "user research, discovery"
        },
        "product-ux": {
            "parent": "product",
            "keywords": ["ux", "design", "frontend", "ui"],
            "experts": ["Don Norman", "Lenny Rachitsky"],
            "test_focus": "UX design, usability"
        },

        # Agent subcategories
        "agent-context": {
            "parent": "agent",
            "keywords": ["context", "memory", "compression", "fundamentals"],
            "experts": ["Andrew Ng"],
            "test_focus": "context management, memory"
        },
        "agent-workflow": {
            "parent": "agent",
            "keywords": ["workflow", "multi-agent", "dispatch", "parallel"],
            "experts": ["Ethan Mollick"],
            "test_focus": "workflow design, coordination"
        },
        "agent-tool": {
            "parent": "agent",
            "keywords": ["tool", "mcp", "function-calling", "api"],
            "experts": ["Simon Willison"],
            "test_focus": "tool use, API integration"
        },
        "agent-bdi": {
            "parent": "agent",
            "keywords": ["bdi", "mental-states", "belief", "desire", "intention"],
            "experts": ["Andrew Ng", "Ethan Mollick"],
            "test_focus": "BDI architecture, reasoning"
        },

        # DevOps subcategories
        "devops-skill-mgmt": {
            "parent": "devops",
            "keywords": ["skill-manager", "skill-sync", "skill-evolution", "planning", "file-based", "task-plan"],
            "experts": ["Kelsey Hightower"],
            "test_focus": "skill lifecycle management, task planning"
        },
        "devops-mcp": {
            "parent": "devops",
            "keywords": ["mcp", "protocol", "server", "builder"],
            "experts": ["Charity Majors"],
            "test_focus": "MCP server development"
        },

        # Data subcategories
        "data-analysis": {
            "parent": "data",
            "keywords": ["data", "analysis", "scientist"],
            "experts": ["DJ Patil", "Hilary Mason"],
            "test_focus": "data analysis, insights"
        },
        "data-docs": {
            "parent": "data",
            "keywords": ["pdf", "xlsx", "docx", "document"],
            "experts": ["Benn Stancil"],
            "test_focus": "document processing"
        },

        # Video subcategories
        "video-editing": {
            "parent": "video",
            "keywords": ["video", "editing", "剪口播", "剪辑", "高清化", "字幕"],
            "experts": ["This Guy Edits"],
            "test_focus": "video editing workflow"
        },
        "video-media": {
            "parent": "video",
            "keywords": ["media", "download", "image", "photo"],
            "experts": ["Peter McKinnon"],
            "test_focus": "media handling"
        },
        "video-analysis": {
            "parent": "video",
            "keywords": ["video-analyzer", "video-frame-extractor", "frame", "scene", "chapter", "video analysis", "拆解", "关键帧"],
            "experts": ["Casey Neistat"],
            "test_focus": "video analysis / frame extraction / chapterization"
        },
        "video-localization": {
            "parent": "video",
            "keywords": ["video-translate", "translate", "dub", "dubbing", "localize", "localization", "subtitle translation", "视频翻译", "配音", "字幕翻译", "本地化", "re-voice"],
            "experts": ["Netflix Localization"],
            "test_focus": "video translation, dubbing, cross-lingual"
        },
        "video-generation": {
            "parent": "video",
            "keywords": ["remotion", "programmatic video", "react video", "generate video"],
            "experts": ["Remotion team"],
            "test_focus": "programmatic video generation"
        },
        "video-strategy": {
            "parent": "video",
            "keywords": ["video script", "video strategy", "video content", "youtube", "video-content-strategist"],
            "experts": ["MrBeast"],
            "test_focus": "video content strategy and scripting"
        },

        # Audio subcategories
        "audio-tts": {
            "parent": "audio",
            "keywords": ["tts", "text-to-speech", "voice synthesis", "voiceover", "edge-tts", "kokoro", "say", "朗读", "配音", "文字转语音", "语音合成", "mac-tts"],
            "experts": ["Microsoft TTS"],
            "test_focus": "text-to-speech synthesis"
        },
        "audio-voice-clone": {
            "parent": "audio",
            "keywords": ["voice clone", "voice cloning", "zero-shot tts", "f5-tts", "voxcpm", "gpt-sovits", "声音克隆", "语音克隆", "mac-voice-clone"],
            "experts": ["ElevenLabs"],
            "test_focus": "zero-shot voice cloning"
        },
        "audio-asr": {
            "parent": "audio",
            "keywords": ["asr", "speech-to-text", "whisper", "transcription", "transcribe", "subtitle", "srt", "vtt", "字幕生成", "语音转文字", "听写", "mac-whisper"],
            "experts": ["OpenAI Whisper"],
            "test_focus": "speech recognition / transcription"
        },
        "audio-processing": {
            "parent": "audio",
            "keywords": ["audio clean", "denoise", "demucs", "loudness", "loudnorm", "mastering", "vocal isolation", "stem separation", "音频清理", "降噪", "响度归一", "母带", "audio-clean"],
            "experts": ["iZotope"],
            "test_focus": "audio cleaning, denoise, mastering"
        },

        # Sales subcategories
        "sales-outreach": {
            "parent": "sales",
            "keywords": ["cold", "outreach", "email", "sequence"],
            "experts": ["Aaron Ross", "Jill Konrath"],
            "test_focus": "cold outreach, sequences"
        },
        "sales-enablement": {
            "parent": "sales",
            "keywords": ["enablement", "revenue", "revops"],
            "experts": ["Mark Roberge"],
            "test_focus": "sales enablement, RevOps"
        },

        # Business subcategories
        "business-strategy": {
            "parent": "business",
            "keywords": ["business", "strategy", "c-level", "ceo"],
            "experts": ["Michael Porter", "Reid Hoffman"],
            "test_focus": "business strategy, planning"
        },
        "business-finance": {
            "parent": "business",
            "keywords": ["finance", "cfo", "financial"],
            "experts": ["Ben Horowitz"],
            "test_focus": "financial planning, analysis"
        },

        # Compliance subcategories
        "compliance-ra": {
            "parent": "compliance",
            "keywords": ["regulatory", "ra", "affairs", "mdr", "fda"],
            "experts": ["Dr. Janet Woodcock", "Graham Law"],
            "test_focus": "regulatory affairs, submissions"
        },
        "compliance-qm": {
            "parent": "compliance",
            "keywords": ["qm", "qms", "iso", "13485", "quality"],
            "experts": ["Trevor Hughes", "Dr. Steven Guttman"],
            "test_focus": "quality management, audits"
        },
        "compliance-security": {
            "parent": "compliance",
            "keywords": ["security", "ciso", "gdpr", "privacy"],
            "experts": ["Dr. Janet Woodcock"],
            "test_focus": "security compliance, privacy"
        },

        # Creative subcategories
        "creative-visual": {
            "parent": "creative",
            "keywords": ["visual", "design", "canvas", "image"],
            "experts": ["Stefan Sagmeister", "Jessica Hische"],
            "test_focus": "visual design, creativity"
        },
        "creative-brainstorm": {
            "parent": "creative",
            "keywords": ["brainstorm", "ideation", "scamper"],
            "experts": ["Aaron Draplin"],
            "test_focus": "creative brainstorming"
        },
    }

    # Assign skills to subcategories
    subcategory_assignments = {subcat: [] for subcat in subcategories.keys()}
    unassigned = []

    for skill in analyzed_skills:
        keywords = skill.get("keywords", [])
        name = skill.get("name", "").lower()
        skill_id = skill.get("id", "")
        tags = skill.get("tags", [])

        best_match = None
        best_score = 0

        for subcat_key, subcat_info in subcategories.items():
            cat_keywords = subcat_info["keywords"]
            score = 0

            # Check keyword matches
            for kw in cat_keywords:
                if kw in name or kw in keywords or kw in tags:
                    score += 2
                # Partial match
                if any(kw in tag for tag in tags):
                    score += 1

            if score > best_score:
                best_score = score
                best_match = subcat_key

        if best_match and best_score > 0:
            subcategory_assignments[best_match].append(skill)
        else:
            unassigned.append(skill)

    # Create cluster objects with subcategory hierarchy
    result = []
    cluster_counter = 1

    for subcat_key, skills in subcategory_assignments.items():
        if skills:
            subcat_info = subcategories[subcat_key]
            result.append({
                "id": f"cluster-{cluster_counter:03d}-{subcat_key}",
                "name": subcat_key,
                "parent_category": subcat_info["parent"],
                "description": f"{subcat_key.replace('-', ' ').title()} - {subcat_info['test_focus']}",
                "skills": skills,
                "skill_count": len(skills),
                "experts": subcat_info["experts"],
                "test_focus": subcat_info["test_focus"]
            })
            cluster_counter += 1

    # Handle unassigned skills as "other"
    if unassigned:
        result.append({
            "id": f"cluster-{cluster_counter:03d}-other",
            "name": "other",
            "parent_category": "other",
            "description": "Other uncategorized skills",
            "skills": unassigned,
            "skill_count": len(unassigned),
            "experts": ["General AI Assistant"],
            "test_focus": "general capabilities"
        })

    return result


STOPWORDS = {
    'this', 'that', 'with', 'for', 'from', 'into', 'during', 'before', 'after',
    'above', 'below', 'between', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 'just', 'also', 'now', 'about', 'over', 'any', 'being', 'have', 'has',
    'had', 'having', 'do', 'does', 'did', 'doing', 'would', 'could', 'should', 'may',
    'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'without',
    'skill', 'skills', 'ability', 'abilities', 'expert', 'pro', 'senior'
}
