# Reverse Skill — Trigger Keywords 速查

完整列表见 [`external/reverse-skill/RULES.md`](../../external/reverse-skill/RULES.md) 第 60-90 行的 "Trigger Keywords (ANY match triggers routing) — Bilingual / 中英双语" 段。

## 通用分类

| 类别 | 关键词示例 |
|---|---|
| **APK / Android** | APK, Android reverse, 反编译, smali, jadx, apktool, Frida, Hook |
| **iOS / Mobile** | iOS reverse, iOS 逆向, Objection, jailbreak detect bypass |
| **Binary / Reverse** | binary analysis, 二进制分析, IDA, radare2, r2, disassembly, 反汇编, reverse engineering, 逆向工程, RE, source recovery, 还原源码 |
| **JS / Frontend** | frontend signature, 前端签名, encrypted params, 加密参数, JS reverse, JS 逆向, jshookmcp, CDP, SourceMap |
| **Packet capture** | packet capture, 抓包, HTTP capture, HTTP 捕获, request replay, 请求重放, anything-analyzer |
| **Web Pentest** | CTF, Pwn, web pentest, Web 渗透, exploit, 漏洞利用, privilege escalation, 提权 |
| **MCP / Agent security** | MCP reverse tools, idalib-mcp, repackage, 重打包, certificate pinning, 证书校验, root detection, 反调试 |
| **Native** | .so analysis, native hook, JNI |
| **General security** | penetration testing, 渗透测试, red team, 红队, security assessment, 安全评估, blue team, 蓝队, incident response, 应急响应 |
| **Reporting** | report/docs generation in security context, 安全上下文中的报告/文档, writeup, pentest report, 渗透报告 |
| **Browser automation** | security browser automation, 安全测试浏览器自动化, Playwright pentest, agent-browser recon |
| **1day / Nday** | N-day, patch diff, 补丁差分, CVE reproduction, 1day, ghidriff, Diaphora |
| **Pwn** | pwn, stack overflow, 栈溢出, heap overflow, ROP, ret2libc, pwntools, GEF, pwndbg, kernel pwn |
| **Firmware** | firmware, 固件, IoT, binwalk, unblob, squashfs, EMBA, UART, JTAG, embedded exploitation |
| **EDR bypass** | EDR bypass, EDR 绕过, AV bypass, 免杀, unhook, direct syscall, indirect syscall, AMSI patch, ETW patch |
| **Scanning / Cracking** | port scan, 端口扫描, Nmap, vulnerability scan, 漏洞扫描, Nuclei, SQL injection, SQL 注入, SQLMap, directory brute force, 目录爆破, FFUF, password cracking, 密码破解, Hashcat, Hydra, Metasploit, Impacket |
| **Bug bounty** | SRC, Bug Bounty, 众测, WAF bypass, 绕过 WAF, IDOR, 越权 |
| **BurpSuite** | BurpSuite, Burp MCP, Intruder, Repeater, Collaborator, proxy history, 代理历史 |
| **LLM / AI security** | LLM security, LLM 安全, AI security testing, Prompt injection, Prompt 注入, jailbreak, 越狱, Agent security, Agent 安全, agent skills security, Agentic Skills Top 10, skill supply chain, 恶意 skill, MCP supply chain |
| **OWASP / Standards** | OWASP LLM Top 10, ASI Top 10, Agentic AI, tool abuse, memory poisoning, garak, PyRIT, promptfoo |
| **API** | API security, API 安全, GraphQL, JWT attack, JWT 攻击, supply chain security, 供应链安全 |
| **Malware** | YARA, malware analysis, 恶意软件分析, AI decompilation, AI 反编译 |
| **Windows / AD** | internal network, 内网渗透, lateral movement, 横向移动, domain penetration, 域渗透, AD attack, BloodHound |
| **Credential** | privilege escalation, 权限提升, credential extraction, 凭证提取, Mimikatz, Kerberoasting, DCSync |
| **C2 / Persistence** | C2, persistence, 持久化, Cobalt Strike, Sliver, Havoc |
| **Game** | game reverse, 游戏逆向, anti-cheat, 反作弊, Unity, IL2CPP, Cheat Engine |
| **.NET** | .NET reverse, C# 逆向, dnSpy, dnSpyEx, de4dot, ConfuserEx, SmartAssembly, .NET Reactor, dnlib, IL patch, SharpHound, Rubeus |
| **Symbol / Diff** | symbol migration, 符号迁移, bindiff, cross-version, PDB missing |
| **Diagram** | security diagram, 安全图表, attack path diagram, 攻击路径图, security architecture, 安全架构图 |

## 路由决策表

按用户首条 query 命中上述关键词 → 路由到对应 [`external/reverse-skill/skills/<场景>/SKILL.md`](../../external/reverse-skill/skills/)。

**模糊场景**：读 `external/reverse-skill/skills/routing.md` 完整路由矩阵（3 维匹配：target type / user intent / toolchain）。

---

> **来源**：本列表来自 reverse-skill RULES.md 第 60-90 行，由 ultraskills 在 [`references/trigger-keywords.md`](references/trigger-keywords.md) 复刻便于阅读。原版权属 zhaoxuya520，遵循 MIT。