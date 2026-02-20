# Contributing to MiFlasher

Thank you for your interest in contributing! MiFlasher is a community-driven project and every contribution — no matter how small — makes a difference.

This document explains how to get started, what we're looking for, and how to submit your work.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Release Process](#release-process)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to making MiFlasher a welcoming space for everyone.

---

## Ways to Contribute

You don't have to write code to contribute. Here's what we need:

| Type | Examples |
|---|---|
| 🐛 **Bug Reports** | Device compatibility issues, crash reports, unexpected behavior |
| 💡 **Feature Requests** | New commands, device support, UI improvements |
| 🔧 **Code** | Bug fixes, new features, refactoring, performance |
| 📖 **Documentation** | README improvements, tutorials, translations |
| 🧪 **Testing** | Testing on different devices/ROMs, reporting edge cases |
| 🎨 **Design** | GUI improvements, UX suggestions |
| 💬 **Community** | Answering issues, helping other users |

---

## Development Setup

### Prerequisites

- Android device with [Termux](https://f-droid.org/packages/com.termux/) (F-Droid version)
- **OR** a Linux/macOS machine with Python 3.10+
- Git

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/djunekz/miflasher
cd miflasher
```

### 2. Set Up Python Environment

**On Termux:**
```bash
pkg update && pkg install python git android-tools
pip install requests --break-system-packages
```

**On Linux/macOS (for developing without a device):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

### 3. Run MiFlasher

```bash
# Make executable
chmod +x miflasher

# Test it runs
./miflasher --help
./miflasher --version
```

### 4. Set Up Remote

```bash
git remote add upstream https://github.com/djunekz/miflasher
git fetch upstream
```

---

## Project Structure

Understanding where things live before you start:

```
miflasher/
├── miflasher              # CLI entry point — argument parsing, routing
│
├── core/
│   ├── logger.py          # ALL output goes through here — do not use print()
│   ├── device.py          # Device detection, ADB/Fastboot wrappers
│   ├── flash.py           # Flash logic — ROM, boot, payload, etc.
│   ├── downloader.py      # HTTP downloader with resume + checksum
│   ├── unlock.py          # Thin unlock manager (delegates to modules/)
│   ├── backup.py          # Backup & restore logic
│   ├── wipe.py            # Wipe logic
│   ├── config.py          # Config read/write
│   ├── session.py         # Session log management
│   └── banner.py          # ASCII art only — keep it simple
│
├── modules/
│   └── miunlock_wrapper.py  # Mi Account flow — self-contained
│
└── gui/
    └── app.py             # Entire web GUI — HTML + CSS + JS + HTTP server
```

**Key principles:**
- `core/` modules are imported by the CLI and GUI
- `modules/` are heavier, optional integrations
- `gui/app.py` should remain a single self-contained file
- Never import from `gui/` inside `core/`

---

## Coding Standards

### Python Style

We follow [PEP 8](https://peps.python.org/pep-0008/) with a few exceptions:

```python
# ✅ Good — descriptive, typed, docstring
def flash_boot(self, path: str, slot: str = "all") -> bool:
    """Flash a boot image to specified slot(s)."""
    if not os.path.exists(path):
        self.log.error(f"File not found: {path}")
        return False
    ...

# ❌ Bad — no types, no docstring, vague name
def do_flash(path, s="all"):
    if not os.path.exists(path):
        print("error")
        return
```

**Rules:**
- Use **type hints** on all function signatures
- Write **docstrings** on all public methods
- Use `self.log` (never `print()`) for all output in core modules
- Handle all exceptions explicitly — no bare `except:` clauses
- Return `bool` for success/failure operations
- Lines max 100 characters

### Logging

Always use the logger, never `print()` directly in core code:

```python
# ✅ Correct
self.log.info("Starting download...")
self.log.success(f"Downloaded {filename}")
self.log.warning("Checksum skipped")
self.log.error(f"File not found: {path}")
self.log.step(1, 3, "Extracting ROM...")  # for numbered steps

# ❌ Never
print("Starting download...")
print(f"ERROR: {e}")
```

### Error Handling

```python
# ✅ Good — specific exceptions, informative messages
try:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
except subprocess.TimeoutExpired:
    self.log.error(f"Command timed out after 30s: {' '.join(cmd)}")
    return False
except FileNotFoundError:
    self.log.error(f"Command not found: {cmd[0]}")
    self.log.info("Install with: pkg install android-tools")
    return False

# ❌ Bad — swallows errors silently
try:
    subprocess.run(cmd)
except:
    pass
```

### Subprocess Calls

All subprocess calls should go through a helper that handles timeouts and errors:

```python
def _run(self, cmd: list, timeout: int = 30) -> tuple:
    """Returns (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -1, "", f"not found: {cmd[0]}"
    except Exception as e:
        return -1, "", str(e)
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(flash): add support for super partition flashing
fix(device): handle devices without A/B slot support
docs(readme): add FAQ entry for Magisk patching
fix(unlock): handle KeyboardInterrupt in _prompt_login
refactor(logger): extract progress bar into separate method
```

---

## Submitting Changes

### For Small Changes (typos, docs, simple fixes)

1. Fork the repo
2. Make changes directly on a branch
3. Submit a PR

### For Larger Changes (new features, refactors)

1. **Open an issue first** — describe what you want to build and why
2. Wait for maintainer feedback / approval
3. Fork and create a feature branch: `git checkout -b feat/super-partition`
4. Make your changes
5. Test on a real device if possible
6. Submit PR referencing the issue

### Branch Naming

```
feat/description      # New features
fix/description       # Bug fixes
docs/description      # Documentation
refactor/description  # Code refactoring
test/description      # Test additions
```

---

## Issue Guidelines

### Before Opening an Issue

1. **Search existing issues** — your problem may already be reported
2. **Check the FAQ** in [README.md](README.md#-faq)
3. **Check your setup** — is `adb` installed? Is USB Debugging enabled?

### Bug Reports

Use the **Bug Report** issue template. Include:

```markdown
**MiFlasher version:** v2.0.0
**Device:** Redmi Note 12 Pro (ruby)
**Android version:** 13
**MIUI version:** MIUI 14.0.6
**Termux version:** 0.118.1

**What I did:**
miflasher flash boot --path boot.img

**Expected behavior:**
Boot image should flash successfully

**Actual behavior:**
[ERROR] Command failed: fastboot flash boot boot.img
FAILED (remote: 'partition not found')

**Full log output:**
<paste output here>
```

### Feature Requests

Use the **Feature Request** template. Include:

- What problem does this solve?
- Who would use this?
- How should it work? (CLI flags, GUI button, etc.)
- Are there any alternatives you've considered?

### Device Compatibility Reports

Found a device that works or doesn't work? Open a **Compatibility Report**:

- Device name, codename, and MIUI version
- Which commands work / don't work
- Any errors or unexpected behavior

---

## Pull Request Guidelines

### PR Checklist

Before submitting, make sure:

- [x] Code follows the [Coding Standards](#coding-standards) above
- [x] All new functions have type hints and docstrings
- [x] No bare `print()` calls in `core/` or `modules/`
- [x] Error handling covers edge cases
- [x] Tested on a real device (or clearly noted that it wasn't)
- [x] PR description explains **what** and **why**
- [z] Commit messages follow conventional commits format
- [z] No unrelated changes in the same PR

### PR Description Template

```markdown
## What does this PR do?
Brief description of the changes.

## Why?
What problem does this solve? Link to related issue if any. Closes #123

## How was it tested?
- Tested on: Redmi Note 12 Pro (ruby), MIUI 14.0.6
- Commands tested: `miflasher flash boot`, `miflasher device`
- Edge cases covered: no device connected, wrong file format

## Screenshots / Output (if applicable)
<paste terminal output here>

## Checklist
- [x] Type hints on all new functions
- [x] Docstrings on all public methods
- [x] No bare print() in core modules
- [x] Tested on real device
```

---

## Testing

MiFlasher doesn't have automated tests yet (contributions welcome!). For now, manual testing is expected.

### What to Test

When contributing code changes, test the affected commands on a real device:

| Command area | Test cases |
|---|---|
| `device` | Connected device, no device, ADB mode, Fastboot mode |
| `flash boot` | Valid file, missing file, wrong format, no device |
| `flash rom` | ZIP with script, ZIP without script, URL download |
| `unlock` | Browser login flow, invalid URL, Ctrl+C interrupt |
| `backup` | All partitions, specific partitions, compress flag |
| `wipe` | Each flag, --all, no confirmation, --force |
| `gui` | Page loads, device info updates, all tab panels |
| `config` | Set, get, show, reset, invalid key |

### Testing Without a Device

Many parts of MiFlasher can be tested without a physical device — mock subprocess calls, test URL parsing, test logger output, test config read/write:

```python
# Example: test URL parsing
from modules.miunlock_wrapper import _parse_redirect, _extract_session_id

url = "https://unlock.update.miui.com/sts?d=wb_abc123&auth=xxx&nonce=yyy"
params = _parse_redirect(url)
assert params["d"] == "wb_abc123"
assert _extract_session_id(params) == "wb_abc123"
print("✅ URL parsing OK")
```

---

## Documentation

Documentation improvements are always welcome.

### What needs docs?

- New commands or flags → update [README.md](README.md)
- New config options → update the config reference table
- Complex behavior → add an FAQ entry
- Non-obvious code → add inline comments
- New modules → add module-level docstring explaining purpose

### Documentation Style

- Use **second person** ("you can", "run this command")
- Use **present tense** ("this command shows", not "this command will show")
- Include **real examples** — copy-pasteable commands
- Use **notes/warnings** for dangerous operations
- Keep language **simple and direct** — not everyone is a native English speaker

---

## Release Process

> *For maintainers only*

1. Update version in `core/banner.py` and `miflasher` (version string)
2. Update `CHANGELOG.md` with all changes since last release
3. Tag the release: `git tag -a v2.1.0 -m "Release v2.1.0"`
4. Push tag: `git push origin v2.1.0`
5. Create GitHub Release with changelog notes

---

## Questions?

- Open a [Discussion](https://github.com/djunekz/miflasher/discussions) for general questions
- Open an [Issue](https://github.com/djunekz/miflasher/issues) for bugs or feature requests
- For security issues, see [SECURITY.md](SECURITY.md)

Thank you for making MiFlasher better! 🚀
