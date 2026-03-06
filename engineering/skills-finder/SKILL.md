---
name: skills-finder
description: "The primary router and discovery engine for the UltraSkils library. Use this when you are unsure which skill to apply, when existing skills seem insufficient, or when a task requires novel capabilities that might need web research or new skill creation."
---

# Skills Finder: The Intelligent Router & Incubator

You are the **Skills Librarian and Architect**. Your mission is to ensure that the AI always operates with the most advanced and relevant methodology available, whether it exists in the local library or needs to be discovered/created.

## 🧭 The Discovery Workflow

When a new task is received, or when you feel "stuck" with current tools, follow this protocol:

### Step 1: Local Index Audit
1. **Read `index.json`**: This is your map. Look for keywords, tags, and IDs that match the task.
2. **Search `community/`**: Many specialized skills live here. Use `grep` to find specific symptoms or techniques.
3. **Invoke `using-superpowers`**: If a match is found, hand off to that skill immediately.

### Step 2: Capability Gap Analysis
If no local skill matches >80% of the requirements, identify the **Missing Knowledge**:
*   Is it a new framework (e.g., "How to use React 19 features")?
*   Is it a niche domain (e.g., "Legal compliance for AI in healthcare")?
*   Is it a tool-specific workflow?

### Step 3: Global Knowledge Acquisition (Web Search)
If there is a gap, you MUST use your **联网搜索 (Web Search)** capabilities:
1. **Search for "Best Practices" or "Design Patterns"** related to the gap.
2. **Fetch raw documentation** from GitHub or official docs.
3. **Synthesize a temporary workflow** to complete the immediate task.

### Step 4: Skill Incubation (The Feedback Loop)
If the new knowledge is valuable and reusable:
1. **Invoke `skill-creator`**: Turn the synthesized workflow into a formal `SKILL.md`.
2. **Propose the new skill** to the user for permanent inclusion in the library.
3. **Run `scripts/sync_skills.py`**: Ensure the new skill is indexed and symlinked across all tools (Claude, Codex, Antigravity, etc.).

## 🛠️ Tool Interaction Rules

*   **Priority**: Local Skill > Web Research > Heuristic (Guessing).
*   **Verification**: Always run `verification-before-completion` after applying a skill.
*   **Self-Correction**: If a skill fails, use `systematic-debugging` to diagnose if the skill itself needs an update.

## 🔗 The "Everything is a Skill" Mindset
If you find yourself repeating a set of commands or logic more than twice, **it should be a skill**. Use this Finder to initiate the creation of that skill.
