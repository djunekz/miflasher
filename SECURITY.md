# Security Policy

## Supported Versions

Only the latest release of MiFlasher receives security updates.

| Version | Supported |
|---------|-----------|
| 2.x (latest) | ✅ Yes |
| 1.x | ❌ No — please upgrade |

---

## Scope

MiFlasher is a command-line tool that:
- Executes `adb` and `fastboot` subprocesses
- Makes HTTP requests to Xiaomi's servers and download URLs
- Reads and writes files on local storage
- Serves a local web dashboard on `localhost`

Security issues we consider **in scope:**

- **Command injection** via unsanitized user input passed to subprocess calls
- **Path traversal** in file path handling (backup/restore/flash)
- **Malicious ROM URL** handling — ensuring downloaded files are properly verified
- **Local web server** (GUI) vulnerabilities — XSS, CSRF, open redirect
- **Credential handling** — Mi Account session tokens stored or logged insecurely
- **Dependency vulnerabilities** in `requests` or other packages
- **Insecure defaults** — e.g., binding the GUI to `0.0.0.0` by default

Issues **out of scope:**

- Vulnerabilities in `adb`, `fastboot`, or Android firmware itself
- Xiaomi server-side security issues
- Social engineering attacks
- Issues requiring physical access to an already-compromised device
- Theoretical issues without a practical exploit

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report privately using one of these methods:

### Option 1: GitHub Private Security Advisory (Preferred)

1. Go to the repository **Security** tab
2. Click **"Report a vulnerability"**
3. Fill in the advisory form with full details

This creates a private thread between you and the maintainers.

### Option 2: Email

Send a detailed report to:

```
security@[project-domain]  (replace with actual address)
```

Encrypt your email using our PGP key if the content is sensitive:

```
(PGP public key block here — replace with actual key)
```

---

## What to Include in Your Report

A good vulnerability report includes:

- **Description** — what the vulnerability is and its impact
- **Affected versions** — which version(s) are affected
- **Steps to reproduce** — clear, minimal reproduction steps
- **Proof of concept** — code snippet or command demonstrating the issue
- **Suggested fix** — if you have one (optional but appreciated)
- **Your contact info** — for follow-up questions

**Example report structure:**

```markdown
## Summary
Command injection in `miflasher flash rom` via maliciously named ROM file.

## Affected Versions
v2.0.0 and earlier

## Reproduction Steps
1. Create a file named `; rm -rf ~; #.zip`
2. Run: miflasher flash rom --path "; rm -rf ~; #.zip"
3. Observe shell command executed

## Impact
Arbitrary command execution with user privileges.

## Suggested Fix
Use subprocess list form (not shell=True) and validate file paths before use.
```

---

## Response Timeline

We take security reports seriously and aim to respond promptly:

| Stage | Timeline |
|---|---|
| **Acknowledgement** | Within 48 hours |
| **Initial assessment** | Within 5 business days |
| **Status update** | Every 7 days until resolved |
| **Fix & release** | Within 30 days for critical issues |

If you don't hear back within 48 hours, follow up via GitHub Discussions.

---

## Disclosure Policy

We follow **coordinated disclosure**:

1. You report privately → we acknowledge within 48 hours
2. We investigate and develop a fix
3. We release the fix and update the changelog
4. We publicly credit you (unless you prefer to remain anonymous)
5. You may publish details 14 days after the fix is released, or sooner with our agreement

We will **never** take legal action against security researchers acting in good faith under this policy.

---

## Security Best Practices for Users

To use MiFlasher safely:

### Download ROMs from trusted sources only
```bash
# Always verify checksums before flashing
# Most ROM providers publish MD5/SHA256 on their download pages
miflasher flash rom --path rom.zip  # auto-verifies if checksum provided
```

### Don't expose the GUI to your network
```bash
# Safe — localhost only (default)
miflasher gui

# Potentially unsafe — other devices on your network can access it
miflasher gui --host 0.0.0.0
```

### Keep your Mi Account session private
- Never share the redirect URL you paste during `miflasher unlock`
- Session tokens are not stored by MiFlasher, but they are visible in terminal history
- Clear terminal history after sensitive operations: `history -c`

### Verify you're running the official tool
```bash
# Check the git log to verify you have unmodified code
git log --oneline -5
git remote -v
```

### Keep dependencies updated
```bash
pip install --upgrade requests --break-system-packages
pkg upgrade android-tools
```

---

## Known Security Considerations

These are known design trade-offs, not exploitable vulnerabilities:

| Consideration | Status | Notes |
|---|---|---|
| GUI runs over HTTP (not HTTPS) | By design | GUI binds to localhost only by default. For network access, use a reverse proxy with TLS. |
| Session tokens visible in terminal | By design | Clear history after use if on a shared device. |
| ROM flash scripts run without sandboxing | By design | `flash_all.sh` scripts from ROM ZIPs are executed as-is. Only flash ROMs from trusted sources. |
| ADB commands executed with user privileges | By design | ADB itself provides full device access. |

---

## Credits

We publicly thank security researchers who responsibly disclose vulnerabilities:

| Researcher | Issue | Version Fixed |
|---|---|---|
| *(your name could be here)* | — | — |

---

## Attribution

This security policy is adapted from the [GitHub Security Advisory](https://docs.github.com/en/code-security/security-advisories) guidelines and follows responsible disclosure best practices.
