#!/usr/bin/env python3
"""
arena_cluster_score.py - 语义聚类 + 评分排名

基于 skill 的 id/description/tags/path 做规则聚类（无需 LLM API），
然后按评分维度（文档完整性、功能明确性、可维护性）打分。

输出:
  skill-arena/clusters.json   - 聚类结果
  skill-arena/scores.json     - 每个 skill 的评分
  skill-arena/winners.json    - 每个 cluster 的获胜者
"""

import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
ARENA_DIR = ROOT / "skill-arena"

# ──────────────────────────────────────────────
# 聚类规则：(cluster_id, cluster_name, 匹配规则)
# 规则：关键词匹配 id 或 tags (不含 path，避免 devops/ 目录路径误匹配)
#
# IMPORTANT: 规则按优先级排列，第一个匹配的生效。
# 具体规则必须放在宽泛规则之前。
# ──────────────────────────────────────────────
CLUSTER_RULES = [
    # ── 先处理 Skills Ecosystem（路径在 devops/，必须先于 engineering-devops）
    ("skills-mgmt",            "Skills·管理",          ["skill-manager", "skill-sync", "skill-creator", "skill-scout", "skill-evolution", "github-to-skill", "writing-skill", "skill-template", "find-skill", "using-superpowers",
                                                         "skills-finder", "claude-md-improver", "claude-automation", "claude-opus-migration", "command-develop", "hook-develop", "plugin-setting", "plugin-struct",
                                                         "context-engineering-collection", "ultraskills-hub", "skill-loader", "gh-fix-ci"]),
    ("skills-browser",         "Skills·浏览器",        ["gstack", "browse", "playwright", "connect-chrome", "setup-browser"]),
    ("skills-web",             "Skills·联网",          ["web-access", "agent-reach", "media-download"]),

    # ── Agent PUA（路径也在 devops/，先于 engineering-devops）
    ("agent-pua",              "Agent·激励强化",       ["pua", "pua-en", "pua-ja", "prompt-optim", "prompt-engineer"]),

    # ── AgentHub 工作流命令（init/spawn/merge 等，先于 engineering-devops 兜底）
    ("agent-agenthub",         "Agent·AgentHub协作",   ["agenthub", "dbs-agent-migration", "dbs-chatroom", "dbs-hook", "dbs-action",
                                                         "dbs-diagnosis", "dbs-slowisfast", "dbs-xhs-title", "dbs-ai-check",
                                                         "dbs-content", "dbs-chatroom-austrian", "dbs-deconstruct", "dbs-"]),

    # Engineering / Code
    ("engineering-code",       "工程·代码质量",        ["code-review", "karpathy-coder", "refactor", "simplif", "focused-fix", "code-tour", "senior-security", "senior-frontend", "senior-backend", "senior-ml", "prompt-governance"]),
    ("engineering-testing",    "工程·测试",             ["tdd", "test-driven", "benchmark", "skill-arena", "gstack-openclaw-retro", "writing-hookify"]),
    ("engineering-qa",         "工程·QA",               ["-qa", "qa-only", "webapp-test", "devex-review", "health", "verification-before"]),
    ("engineering-debug",      "工程·调试",             ["systematic-debug", "investigate", "careful", "guard"]),
    ("engineering-git",        "工程·Git工作流",        ["git-commit-master", "bfg-repo", "clean-gone", "commit-push", "finishing-a-dev", "using-git-worktree", "requesting-code-review", "receiving-code-review"]),
    ("engineering-frontend",   "工程·前端",             ["frontend-design", "web-artifact", "canvas-design", "theme-factory", "design-html"]),
    # NOTE: "devops" keyword removed — it matched the devops/ directory PATH causing false positives
    # (pua, skill-manager etc. all live in devops/ directory)
    ("engineering-devops",     "工程·DevOps",           ["docker", "k8s", "kubernetes", "setup-deploy", "land-and-deploy", "ship", "canary", "infra", "azure-cloud", "aws-solution", "gcp-cloud",
                                                          "devops-engineer", "kubernetes-specialist", "senior-devops", "helm-chart", "terraform", "observability",
                                                          "release-manager", "git-worktree-manager", "ms365", "google-workspace",
                                                          "incident-response", "gh-fix-ci"]),
    ("engineering-security",   "工程·安全",             ["security", "cso", "ciso-advisor", "secret", "vuln", "pentest", "ai-security"]),
    ("engineering-arch",       "工程·架构",             ["architect", "system-design", "ddd", "microservice", "mcp-builder", "mcp-integration", "mcp-cli"]),
    ("engineering-ml",         "工程·ML/AI",            ["machine-learning", "model-train", "llm-cost", "llm-wiki", "hugging-face", "huggingface", "gradio", "trackio"]),
    ("engineering-mobile",     "工程·移动",             ["mobile", "react-native", "flutter-expert", "kotlin-specialist", "swift-expert"]),

    # L2-aware fullstack subclusters — specific language/framework specialists
    ("engineering-lang",       "工程·语言专家",         ["python-pro", "javascript-pro", "typescript-pro", "golang-pro", "rust-engineer", "cpp-pro", "csharp-developer", "php-pro", "kotlin-specialist", "swift-expert"]),
    ("engineering-framework",  "工程·框架专家",         ["react-expert", "vue-expert", "nextjs-developer", "nestjs-expert", "django-expert", "fastapi-expert", "rails-expert", "spring-boot-engineer", "laravel-specialist"]),
    ("engineering-platform",   "工程·平台开发",         ["salesforce-developer", "shopify-expert", "wordpress-pro", "atlassian-mcp"]),
    ("engineering-fullstack",  "工程·全栈工程师",       ["fullstack", "full-stack", "senior-fullstack", "karpathy-coder",
                                                          "api-designer", "code-documenter", "feature-forge", "spec-miner", "legacy-modernizer",
                                                          "ml-pipeline", "monitoring-expert", "cli-developer", "game-developer", "fine-tuning-expert",
                                                          "debugging-wizard", "chaos-engineer", "websocket-engineer", "embedded-systems",
                                                          "database-optimizer", "test-master", "mcp-developer", "postgres-pro", "sql-pro",
                                                          "pandas-pro", "spark-engineer", "sre-engineer", "the-fool"]),

    # Agent / AI Architecture
    ("agent-arch",             "Agent·架构",            ["multi-agent-pattern", "bdi-mental", "dispatching-parallel", "subagent-driven", "agent-optim"]),
    ("agent-context",          "Agent·上下文管理",      ["context-compress", "context-optim", "context-degrad", "context-fundament", "latent-brief", "filesystem-context"]),
    ("agent-memory",           "Agent·记忆系统",        ["memory-system", "checkpoint", "project-develop"]),
    ("agent-eval",             "Agent·评估",            ["advanced-eval", "evaluation", "agent-eval"]),
    ("agent-workflow",         "Agent·工作流",          ["executing-plan", "writing-plan", "autoplan", "planning-with-files", "skill-development", "agent-development", "e2e-development"]),
    ("agent-hosted",           "Agent·托管运行",        ["hosted-agent", "pair-agent", "claude-session-driver", "driving-claude", "tool-design"]),

    # Content / Writing
    ("content-writing",        "内容·写作",             ["writing", "doc-coauthor", "document-release", "internal-comm", "copy-edit", "proofreading", "article-edit", "script-polish", "caveman-help"]),
    ("content-seo",            "内容·SEO",              ["seo", "schema-markup", "programmatic-seo", "ai-seo"]),
    ("content-social",         "内容·社交媒体",         ["social-content", "x-master", "article-to-x", "xhs-image", "wechat-image", "huashu-xhs", "huashu-wechat", "topic-gen", "khazix-writer", "huashu-article-to-x",
                                                          "baoyu-post-to-wechat", "baoyu-post-to-weibo", "baoyu-post-to-x", "baoyu-translate", "baoyu-url-to-markdown", "baoyu-danger-x-to-markdown", "baoyu-format-markdown",
                                                          "baoyu-youtube-transcript", "baoyu-danger-gemini-web"]),
    ("content-video",          "内容·视频",             ["video", "剪", "字幕", "remotion", "image-to-video", "video-frame", "video-split", "video-outline", "video-check", "douyin-script", "huashu-douyin", "huashu-video"]),
    ("content-image",          "内容·图像设计",         ["image-analyz", "image-audit", "image-review", "face-beautif", "gemini-image", "photo", "visual-expert", "commercial-director", "algorithmic-art", "huashu-design", "huashu-image", "photography",
                                                          "baoyu-image-gen", "baoyu-imagine", "baoyu-cover-image", "baoyu-article-illustrator", "baoyu-infographic", "baoyu-image-cards", "baoyu-comic"]),
    ("content-doc",            "内容·文档生成",         ["pdf", "docx", "xlsx", "pptx", "slides", "md-to-pdf", "ikea-style-ppt", "huashu-slides", "huashu-md-to-pdf",
                                                          "baoyu-slide-deck", "baoyu-diagram", "baoyu-markdown-to-html"]),
    ("content-presentation",   "内容·演示设计",         ["deck-that-wins", "awesome-design-md", "poster-print-design", "meeting-notes-and-actions", "spreadsheet-formula-helper", "to-prd"]),

    # Design (including design tool skills from misc)
    ("design-ux",              "设计·UX/产品设计",      ["design-review", "design-consult", "design-shotgun", "plan-design", "ikea-designer",
                                                          "ui-ux-pro-max-skill", "design-tokens", "figma-to-code", "icon-system", "motion-design"]),

    # Marketing
    ("marketing-cro",          "营销·转化率优化",       ["page-cro", "signup-flow-cro", "popup-cro", "onboarding-cro", "paywall-upgrade", "form-cro", "cro-advisor"]),
    ("marketing-email",        "营销·邮件",             ["cold-email", "email-sequence"]),
    ("marketing-ads",          "营销·广告",             ["ad-creative", "paid-ads", "ab-test-setup"]),
    ("marketing-analytics",    "营销·增长分析",         ["analytics-tracking", "revenue-op", "churn-prev", "referral-program"]),
    ("marketing-strategy",     "营销·策略",             ["launch-strateg", "content-strateg", "pricing-strateg", "free-tool-strateg", "competitor-alt", "product-marketing", "community-marketing", "aso-audit"]),
    ("marketing-copy",         "营销·文案",             ["copywriting", "marketing-psych", "marketing-ideas"]),

    # Business / C-Level
    ("business-clevel",        "商业·高管顾问",         ["c-level", "ceo-advisor", "cto-advisor", "cfo-advisor", "cmo-advisor", "coo-advisor", "chro-advisor", "chief-of-staff", "board-deck", "board-meeting", "founder-coach", "executive-mentor", "company-os", "ma-playbook", "intl-expansion"]),
    ("business-product",       "商业·产品",             ["product-team", "jtbd", "feature", "roadmap", "priorit", "plan-eng-review", "plan-ceo-review", "office-hours"]),
    ("business-strategy",      "商业·战略分析",         ["war-room", "scenario-war", "competitive-intel", "wardley", "decision-logger", "cs-onboard", "cs-wiki"]),
    ("business-finance",       "商业·财务",             ["financial", "budget", "forecast", "cs-financial", "hv-analysis"]),
    ("business-hr",            "商业·人力资源",         ["hiring", "org-health", "change-management", "culture-architect", "internal-narrative", "brand-guidelines"]),
    ("business-legal",         "商业·法务合规",         ["legal", "compliance", "gdpr", "audit-report", "standards"]),
    ("business-pm",            "商业·项目管理",         ["project-management", "scrum", "retro", "retrospective", "aar", "postmortem", "stress-test", "hard-call", "board-prep", "decision"]),

    # Education
    ("education",              "教育·学习研究",         ["learn", "feynman", "socratic", "research", "info-search", "material-search", "huashu-research", "huashu-info", "huashu-material", "huashu-prompt-save", "prompt-save"]),

    # Persona
    ("persona",                "人物·视角模拟",         ["perspective", "nuwa-skill", "nuwa", "x-mastery-mentor", "behuman", "blessing-style"]),

    # Productivity
    ("productivity",           "效率·生产力",           ["eisenhower", "rice", "moscow", "task-analyz", "brainstorm", "scamper", "sixhats", "caveman", "compress", "slack-messaging", "slack-gif", "loop", "dynamic-expert"]),

    # Data
    ("data",                   "数据·分析",             ["data-pro", "huashu-data", "analytic", "report", "pipeline", "revenue-operations", "llm-cost", "data-quality", "statistical", "snowflake", "sql-database", "database-design", "database-schema", "senior-data"]),

    # Voice / Audio (previously scattered in misc)
    ("media-audio",            "媒体·语音音频",         ["mac-tts", "mac-voice-clone", "mac-whisper", "audio-clean"]),

    # 补充兜底规则（宽泛匹配放最后）
    ("engineering-code",       "工程·代码质量",         ["pr-review", "adversarial-review", "a11y-audit", "codebase-onboard", "dependency-audit", "changelog", "monorepo", "runbook", "tech-debt", "performance-profil", "api-test", "spec-driven", "karpathy", "engineering-skill", "engineering-advanced"]),
    ("engineering-devops",     "工程·DevOps",           ["helm-chart-builder", "terraform-patterns", "observability-designer", "incident-commander", "git-worktree-manager"]),
    ("engineering-security",   "工程·安全",             ["red-team", "threat-detect", "secops", "isms-audit", "risk-management"]),
    ("engineering-ml",         "工程·ML/AI",            ["senior-computer-vision", "reasoning-trace", "self-improv", "self-eval", "eval", "extract", "agent-designer", "agent-workflow-designer", "spec-driven"]),
    ("business-clevel",        "商业·高管顾问",         ["board", "business-growth", "business-invest", "saas-metric", "revops", "tech-stack-eval", "epic-design", "digital-brain"]),
    ("business-hr",            "商业·人力资源",         ["sales-engineer", "sales-enablement", "lead-magnet"]),
    ("business-legal",         "商业·法务合规",         ["fda-consultant", "mdr-745", "capa-officer", "isms", "qms", "ra-qm", "quality-manager", "quality-doc", "regulatory", "risk-management"]),
    ("business-pm",            "商业·项目管理",         ["tc-tracker", "skill-tester", "remember"]),
    ("marketing-strategy",     "营销·策略",             ["app-store-optim", "marketing-context", "marketing-demand", "marketing-ops", "marketing-strategy-pmm", "marketing-skill", "finance-skill"]),
    ("content-writing",        "内容·写作",             ["content-creator", "content-humanizer", "content-production", "contract-and-proposal", "email-template", "customer-success"]),
    ("content-social",         "内容·社交媒体",         ["social-media", "x-twitter", "huashu-agent-swarm", "huashu-speech-coach"]),
    ("skills-mgmt",            "Skills·管理",           ["claude-md-management", "command-development", "hook-development", "plugin-structure", "plugin-settings", "context-engineering", "init-skill", "sample-skill", "example-skill", "template-skill"]),
    ("platform-claude-api",    "平台·Claude API",       ["claude-api", "stripe-best", "stripe-integration", "mcp-server-builder", "claude-opus-4-5-migration"]),
    ("agent-agenthub",         "Agent·AgentHub协作",    ["dbs"]),
]

# 兜底：未匹配的归到 misc
MISC_CLUSTER = ("misc", "其他未分类", [])

# ──────────────────────────────────────────────
# L2 子聚类定义
# 对大型 L1 cluster 做功能性细分，供 PK 测试使用
# 格式: cluster_id → list of (subcluster_id, subcluster_name, keyword_list)
# ──────────────────────────────────────────────
L2_SUBCLUSTER_RULES: dict = {
    "engineering-fullstack": [
        ("engineering-fullstack-api",      "API & 后端设计",      ["api-designer", "feature-forge", "spec-miner", "legacy-modernizer", "monitoring-expert", "sre-engineer"]),
        ("engineering-fullstack-db",       "数据库 & 存储",       ["postgres-pro", "sql-pro", "database-optimizer", "pandas-pro", "spark-engineer"]),
        ("engineering-fullstack-tools",    "开发工具 & 基础设施",  ["cli-developer", "mcp-developer", "websocket-engineer", "embedded-systems", "chaos-engineer"]),
        ("engineering-fullstack-testing",  "测试 & 质量",         ["test-master", "debugging-wizard"]),
        ("engineering-fullstack-ml",       "ML & AI 工程",        ["ml-pipeline", "fine-tuning-expert"]),
        ("engineering-fullstack-general",  "通用全栈",            ["the-fool", "code-documenter", "game-developer"]),
    ],
    "engineering-devops": [
        ("engineering-devops-cloud",       "云平台架构",          ["aws-solution", "azure-cloud", "gcp-cloud", "terraform", "helm-chart"]),
        ("engineering-devops-container",   "容器 & K8s",          ["docker", "k8s", "kubernetes", "kubernetes-specialist"]),
        ("engineering-devops-cicd",        "CI/CD & 部署",        ["setup-deploy", "land-and-deploy", "ship", "canary", "release-manager", "senior-devops", "devops-engineer"]),
        ("engineering-devops-observ",      "可观测性 & 事故响应",  ["observability", "incident-response", "monitoring", "incident-commander"]),
        ("engineering-devops-workspace",   "工作区管理",          ["ms365", "google-workspace", "git-worktree-manager"]),
    ],
    "skills-mgmt": [
        ("skills-mgmt-lifecycle",          "Skill 生命周期",      ["skill-manager", "skill-sync", "skill-creator", "skill-evolution", "skill-scout"]),
        ("skills-mgmt-search",             "Skill 搜索 & 发现",   ["ultraskills-hub", "skills-finder", "github-to-skill", "find-skill"]),
        ("skills-mgmt-claude-config",      "Claude 配置工具",     ["claude-md-improver", "claude-automation", "hook-develop", "command-develop", "plugin-setting", "plugin-struct"]),
    ],
    "business-clevel": [
        ("business-clevel-cxo",            "CxO 顾问",            ["ceo-advisor", "cto-advisor", "cfo-advisor", "cmo-advisor", "coo-advisor", "chro-advisor"]),
        ("business-clevel-strategy",       "战略决策",            ["chief-of-staff", "board-deck", "board-meeting", "founder-coach", "executive-mentor", "board", "business-growth"]),
        ("business-clevel-ops",            "运营体系",            ["company-os", "ma-playbook", "intl-expansion", "saas-metric", "revops", "tech-stack-eval"]),
    ],
    "content-social": [
        ("content-social-baoyu",           "Baoyu 内容工具",      ["baoyu-post-to-wechat", "baoyu-post-to-weibo", "baoyu-post-to-x", "baoyu-translate", "baoyu-url-to-markdown",
                                                                    "baoyu-danger-x-to-markdown", "baoyu-format-markdown", "baoyu-youtube-transcript", "baoyu-danger-gemini-web"]),
        ("content-social-platforms",       "社交平台发布",        ["social-content", "x-master", "article-to-x", "xhs-image", "wechat-image", "topic-gen", "khazix-writer"]),
        ("content-social-huashu",          "Huashu 社交矩阵",     ["huashu-xhs", "huashu-wechat", "huashu-article-to-x", "huashu-agent-swarm", "huashu-speech-coach"]),
    ],
    "content-image": [
        ("content-image-baoyu",            "Baoyu 图像生成",      ["baoyu-image-gen", "baoyu-imagine", "baoyu-cover-image", "baoyu-article-illustrator", "baoyu-infographic", "baoyu-image-cards", "baoyu-comic"]),
        ("content-image-analysis",         "图像分析 & 审计",     ["image-analyz", "image-audit", "image-review", "face-beautif", "visual-expert", "photography"]),
        ("content-image-creation",         "AI 图像创作",         ["gemini-image", "commercial-director", "algorithmic-art", "huashu-design", "huashu-image"]),
    ],
    "agent-workflow": [
        ("agent-workflow-planning",        "规划 & 执行",         ["executing-plan", "writing-plan", "autoplan"]),
        ("agent-workflow-files",           "文件驱动工作流",      ["planning-with-files"]),
        ("agent-workflow-development",     "开发辅助工作流",      ["skill-development", "agent-development", "e2e-development"]),
    ],
}


def match_cluster(skill: dict) -> str:
    """根据 id/tags 匹配最佳 cluster。

    NOTE: 不再用 path 匹配，因为 path 包含目录名（如 devops/）
    会导致 pua、skill-manager 等错误归入 engineering-devops。
    """
    sid = skill.get("id", "").lower().strip('"\'')
    tags = [t.lower() for t in (skill.get("tags") or [])]
    # 只用 id + tags 匹配，不包含 path
    text = f"{sid} {' '.join(tags)}"

    for cluster_id, _, keywords in CLUSTER_RULES:
        for kw in keywords:
            if kw in text:
                return cluster_id
    return MISC_CLUSTER[0]


def compute_l2_subclusters(cluster_id: str, skill_ids: list, scores: dict) -> list:
    """计算 L2 子聚类。

    对给定 cluster 的 skills，按 L2_SUBCLUSTER_RULES 中的规则分组。
    规则未覆盖的 skills 归入 "{cluster_id}-other" 子类。

    Args:
        cluster_id: L1 cluster ID
        skill_ids: 该 cluster 的所有 skill ID 列表
        scores: skill ID → score dict

    Returns:
        List of subcluster dicts: [{id, name, skills, winner}]
    """
    rules = L2_SUBCLUSTER_RULES.get(cluster_id)
    if not rules:
        return []

    remaining = set(skill_ids)
    subclusters = []

    for sub_id, sub_name, keywords in rules:
        matched = []
        for sid in list(remaining):
            sid_lower = sid.lower().strip('"\'')
            if any(kw in sid_lower for kw in keywords):
                matched.append(sid)
                remaining.discard(sid)
        if matched:
            ranked = sorted(matched, key=lambda x: scores.get(x, {}).get("total", 0), reverse=True)
            subclusters.append({
                "id": sub_id,
                "name": sub_name,
                "skill_count": len(ranked),
                "winner": ranked[0],
                "skills": ranked,
            })

    # Leftover → other subcluster
    if remaining:
        ranked = sorted(list(remaining), key=lambda x: scores.get(x, {}).get("total", 0), reverse=True)
        subclusters.append({
            "id": f"{cluster_id}-other",
            "name": "其他",
            "skill_count": len(ranked),
            "winner": ranked[0] if ranked else None,
            "skills": ranked,
        })

    return subclusters


# ──────────────────────────────────────────────
# 评分
# ──────────────────────────────────────────────

def score_skill(skill: dict, skill_md_text: str) -> dict:
    """
    评分维度（均为 0-10，最终加权）：
      文档质量 (50%): description 长度、有无示例、有无 tags、body 长度
      功能明确性 (30%): id 清晰、有版本、有 github_url、有 tags
      可维护性 (20%): 有 frontmatter、有 path、有 version
    """
    desc = skill.get("description", "") or ""
    tags = skill.get("tags") or []
    version = skill.get("version") or ""
    github_url = skill.get("github_url") or ""

    body_len = len(skill_md_text)

    # 文档质量 0-10
    doc = 0
    if len(desc) >= 30:    doc += 2
    if len(desc) >= 80:    doc += 1
    if len(desc) >= 150:   doc += 1
    if body_len >= 500:    doc += 2
    if body_len >= 2000:   doc += 1
    if body_len >= 5000:   doc += 1
    # 有示例段落
    if "example" in skill_md_text.lower() or "示例" in skill_md_text or "用法" in skill_md_text:
        doc += 1
    # 有 checklist / 步骤
    if "- [" in skill_md_text or "Step " in skill_md_text or "步骤" in skill_md_text:
        doc += 1
    doc = min(doc, 10)

    # 功能明确性 0-10
    func = 0
    if len(skill.get("id", "")) >= 3:   func += 2
    if len(tags) >= 1:                  func += 2
    if len(tags) >= 3:                  func += 1
    if version:                         func += 2
    if github_url:                      func += 1
    # id 不是纯路径名（有语义）
    if "-" in skill.get("id", ""):      func += 1
    if len(desc) >= 50:                 func += 1
    func = min(func, 10)

    # 可维护性 0-10
    maint = 0
    if "---" in skill_md_text[:50]:     maint += 3   # 有 frontmatter
    if skill.get("path"):               maint += 2
    if version:                         maint += 2
    if github_url:                      maint += 1
    # 有 tags
    if len(tags) >= 2:                  maint += 2
    maint = min(maint, 10)

    total = round(doc * 0.50 + func * 0.30 + maint * 0.20, 2)

    return {
        "doc_quality": doc,
        "func_clarity": func,
        "maintainability": maint,
        "total": total,
    }


def main():
    inventory_file = ARENA_DIR / "skills_inventory.json"
    skills = json.loads(inventory_file.read_text())
    print(f"Loaded {len(skills)} skills")

    # 读取每个 SKILL.md 文本（用于评分）
    skill_texts = {}
    for s in skills:
        path = ROOT / s["path"].lstrip("./")
        try:
            skill_texts[s["id"]] = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            skill_texts[s["id"]] = ""

    # 聚类
    cluster_members = defaultdict(list)
    skill_cluster_map = {}
    for s in skills:
        cid = match_cluster(s)
        cluster_members[cid].append(s["id"])
        skill_cluster_map[s["id"]] = cid

    # 评分
    scores = {}
    for s in skills:
        sid = s["id"]
        scores[sid] = score_skill(s, skill_texts[sid])

    # 每个 cluster 排名找 winner
    winners = {}
    for cid, members in cluster_members.items():
        ranked = sorted(members, key=lambda x: scores[x]["total"], reverse=True)
        winners[cid] = ranked[0] if ranked else None

    # 生成 clusters.json
    cluster_name_map = {r[0]: r[1] for r in CLUSTER_RULES}
    cluster_name_map[MISC_CLUSTER[0]] = MISC_CLUSTER[1]

    clusters_out = []
    for cid, members in sorted(cluster_members.items()):
        ranked = sorted(members, key=lambda x: scores[x]["total"], reverse=True)
        subclusters = compute_l2_subclusters(cid, members, scores)
        entry = {
            "id": cid,
            "name": cluster_name_map.get(cid, cid),
            "skill_count": len(members),
            "winner": winners.get(cid),
            "skills": ranked,  # 按分数排序
        }
        if subclusters:
            entry["subclusters"] = subclusters
        clusters_out.append(entry)
    clusters_out.sort(key=lambda x: x["skill_count"], reverse=True)

    (ARENA_DIR / "clusters.json").write_text(
        json.dumps(clusters_out, ensure_ascii=False, indent=2)
    )
    print(f"Written clusters.json: {len(clusters_out)} clusters")

    # 生成 scores.json（按 total 降序）
    scores_list = []
    for s in skills:
        sid = s["id"]
        sc = scores[sid]
        scores_list.append({
            "id": sid,
            "path": s["path"],
            "cluster": skill_cluster_map[sid],
            "cluster_name": cluster_name_map.get(skill_cluster_map[sid], skill_cluster_map[sid]),
            "is_winner": (winners.get(skill_cluster_map[sid]) == sid),
            **sc,
        })
    scores_list.sort(key=lambda x: x["total"], reverse=True)

    (ARENA_DIR / "scores.json").write_text(
        json.dumps(scores_list, ensure_ascii=False, indent=2)
    )
    print(f"Written scores.json")

    # 生成 winners.json
    winners_list = []
    for cid, wid in sorted(winners.items()):
        if not wid:
            continue
        # 找到该 cluster 的所有排名
        members = cluster_members[cid]
        ranked = sorted(members, key=lambda x: scores[x]["total"], reverse=True)
        defeated = ranked[1:] if len(ranked) > 1 else []
        winners_list.append({
            "cluster": cid,
            "cluster_name": cluster_name_map.get(cid, cid),
            "winner": wid,
            "score": scores[wid]["total"],
            "runner_up": ranked[1] if len(ranked) > 1 else None,
            "total_contestants": len(members),
            "defeated": defeated[:5],  # 最多列5个
        })
    winners_list.sort(key=lambda x: x["score"], reverse=True)

    (ARENA_DIR / "winners.json").write_text(
        json.dumps(winners_list, ensure_ascii=False, indent=2)
    )
    print(f"Written winners.json: {len(winners_list)} category winners")

    # 统计摘要
    print("\n=== ARENA SUMMARY ===")
    print(f"Total skills: {len(skills)}")
    print(f"Total clusters: {len(clusters_out)}")
    avg_score = sum(s["total"] for s in scores_list) / len(scores_list)
    print(f"Avg score: {avg_score:.2f}/10")
    top10 = scores_list[:10]
    print("\nTop 10 skills:")
    for s in top10:
        print(f"  {s['total']:5.2f}  {s['id']:<45} [{s['cluster_name']}]")
    misc_count = len(cluster_members.get("misc", []))
    print(f"\nMisc (unclassified): {misc_count}")
    if misc_count > 0:
        print("  Sample:", cluster_members["misc"][:10])

    # ──────────────────────────────────────────────
    # 低分统计 + 淘汰建议
    # ──────────────────────────────────────────────
    LOW_SCORE_THRESHOLD = 4.0       # 低于此分数视为低质量
    ELIMINATION_THRESHOLD = 3.0     # 低于此分数建议淘汰

    low_performers = [s for s in scores_list if s["total"] < LOW_SCORE_THRESHOLD]
    candidates_for_elimination = [s for s in scores_list if s["total"] < ELIMINATION_THRESHOLD]

    print(f"\n⚠️  Low performers (score < {LOW_SCORE_THRESHOLD}): {len(low_performers)}")
    if low_performers:
        for s in low_performers[:10]:
            print(f"  {s['total']:5.2f}  {s['id']:<45} [{s['cluster_name']}]")
        if len(low_performers) > 10:
            print(f"  ... and {len(low_performers) - 10} more")

    if candidates_for_elimination:
        print(f"\n❌ Elimination candidates (score < {ELIMINATION_THRESHOLD}): {len(candidates_for_elimination)}")
        for s in candidates_for_elimination[:5]:
            print(f"  {s['total']:5.2f}  {s['id']:<45} → consider removing")

    # 加载历史低分记录，累计连续低分次数
    low_perf_file = ARENA_DIR / "low_performers.json"
    history = {}
    if low_perf_file.exists():
        try:
            history = json.loads(low_perf_file.read_text())
        except Exception:
            history = {}

    # 更新：低分 +1，脱离低分则重置
    current_low_ids = {s["id"] for s in low_performers}
    for sid in current_low_ids:
        entry = history.get(sid, {"consecutive_low": 0, "scores": []})
        entry["consecutive_low"] = entry.get("consecutive_low", 0) + 1
        entry["scores"] = (entry.get("scores", []) + [scores[sid]["total"]])[-5:]  # 保留最近5次
        entry["cluster"] = skill_cluster_map.get(sid, "misc")
        history[sid] = entry
    # 脱离低分的重置
    for sid in list(history.keys()):
        if sid not in current_low_ids:
            del history[sid]

    # 标记建议淘汰（连续3次以上低分）
    CONSECUTIVE_LOW_LIMIT = 3
    eliminate_list = []
    for sid, entry in history.items():
        if entry["consecutive_low"] >= CONSECUTIVE_LOW_LIMIT:
            entry["recommendation"] = "eliminate"
            eliminate_list.append(sid)
        elif entry["consecutive_low"] >= 2:
            entry["recommendation"] = "warning"
        else:
            entry["recommendation"] = "monitor"

    low_perf_file.write_text(json.dumps(history, ensure_ascii=False, indent=2))

    if eliminate_list:
        print(f"\n🚨 ELIMINATION RECOMMENDED ({len(eliminate_list)} skills, "
              f"low score ≥{CONSECUTIVE_LOW_LIMIT} consecutive runs):")
        for sid in eliminate_list[:10]:
            h = history[sid]
            print(f"  {sid:<45} avg={sum(h['scores'])/len(h['scores']):.1f} "
                  f"runs={h['consecutive_low']}")
        print(f"\n  To remove: python3 devops/skill-manager/scripts/delete_skill.py <skill-id>")
        print(f"  Then rebuild: python3 scripts/arena_scan.py && "
              f"python3 scripts/arena_cluster_score.py && "
              f"python3 scripts/arena_build_index.py")


if __name__ == "__main__":
    from pipeline_lock import PipelineLock
    with PipelineLock("arena_cluster_score"):
        main()
