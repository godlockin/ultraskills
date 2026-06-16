# SkillSpector Detection Categories

SkillSpector evaluates 64 patterns across 16 categories. Two-stage analysis:
- **Stage 1 (always on):** regex + AST + OSV.dev CVE lookups
- **Stage 2 (optional, `--with-llm`):** LLM semantic filter (~87% precision)

## 16 detection categories

1. **Prompt injection** — direct overrides, role hijacking, instruction smuggling
2. **MCP tool poisoning** — malicious tool descriptions, tool-shadowing attacks
3. **Memory poisoning** — state-persistence exploits, session-hijack patterns
4. **Rogue agent behavior** — self-replication, scope-escape, autonomous goal drift
5. **Data exfiltration** — webhook/URL exfil, env-var scraping, encoded payloads
6. **Supply-chain CVEs** — vulnerable dependency versions via OSV.dev
7. **Credential leakage** — hardcoded API keys, tokens, passwords
8. **Privilege escalation** — sudo/su abuse, file-permission tampering
9. **Filesystem attacks** — path traversal, /etc/ writes, dotfile hijacking
10. **Network attacks** — reverse shells, port scanning, C2 callbacks
11. **Code execution** — eval/exec abuse, dynamic imports, deserialization
12. **Cryptojacking** — hidden miners, hash-rate exfil
13. **Phishing** — credential-harvesting UI, fake auth flows
14. **Resource abuse** — fork bombs, infinite loops, DoS patterns
15. **Obfuscation** — base64/hex blobs, unicode homoglyphs, zero-width chars
16. **Compliance violations** — license conflicts, GDPR/CCPA data handling

## Risk scoring

- Each finding contributes to a 0-100 risk score
- Severity multipliers: critical=25, high=10, medium=3, low=1
- Final score capped at 100
- Bands: SAFE (0-29), CAUTION (30-69), DO NOT INSTALL (≥70 or any critical)

## CI mode

Always use `--no-llm` in CI:
- No API key required
- Stage 1 is sufficient to catch most supply-chain and pattern-based issues
- Stage 2 reserved for human review on borderline CAUTION cases

```bash
python3 devops/skill-security-scan/scripts/run_skillspector.py <path> --no-llm
```

## References

- [NVIDIA/SkillSpector upstream](https://github.com/NVIDIA/SkillSpector)
- [OSV.dev](https://osv.dev) — open-source vulnerability database used in Stage 1
