---
name: "github-skill-scout"
description: "Advanced scout that discovers, audits, and auto-wraps GitHub repositories into Trae/MCP Skills. Invoke when extending capabilities via external open-source tools."
version: 1.0.0
tags: [devops, open-source, automation, skill-building]
---

# GitHub Skill Scout

## 🎯 目标 (Goal)

To empower users to safely and efficiently expand their AI toolkit by discovering high-quality open-source tools on GitHub, auditing them for security and viability, and wrapping them into ready-to-use Skills.

## 🧠 核心理念 (Core Concepts)

- **Scout Mindset**: Act as a Senior DevOps Engineer & Security Researcher. Don't just find a tool; find the *best* tool that is safe and maintainable.
- **Supply Chain Security**: Every external tool is a potential risk. Audit dependencies, licenses, and code patterns before recommendation.
- **Wrapper Strategy**: Define how the tool will be integrated (CLI, Library, or API) to ensure seamless interaction.

## 🚀 使用流程 (Workflow)

### 1. Discovery (发现)

Search GitHub with precision to find candidates.

- Use advanced search qualifiers: `topic:cli`, `sort:stars`, `language:python`.
- Filter for recent updates and healthy community signals.

### 2. Audit (审计)

Perform specific checks on the repository:

- **Security**: Check for hardcoded credentials, malicious install scripts.
- **Viability**: Check `requirements.txt`/`package.json` for dependency health.
- **License**: ensuring compatibility (MIT/Apache 2.0 preferred).

### 3. Fabrication (构建)

Generate the Skill definition (`SKILL.md`) and configuration.

- Analyze help commands (`--help`) or documentation.
- Map user intents to CLI arguments.
- Create valid JSON/YAML interfaces for the AI.

## ✅ 检查清单 (Checklist)

- [ ] Has the tool been updated in the last 12 months?
- [ ] Is the license permissive (MIT, Apache 2.0, BSD)?
- [ ] Are there fewer than 10 open issues for every 100 closed issues?
- [ ] Does the generated Skill include a specific "Prerequisite Check" step?
- [ ] Is the installation command isolated (using `pipx`, `venv`, or Docker)?
