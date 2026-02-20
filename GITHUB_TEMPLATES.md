# GitHub Templates

Place these files in `.github/` directory of your repository.

---

## .github/ISSUE_TEMPLATE/bug_report.md

```markdown
---
name: Bug Report
about: Something isn't working as expected
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
<!-- A clear and concise description of what the bug is -->

## Steps to Reproduce
1. Run command: `miflasher ...`
2. ...
3. See error

## Expected Behavior
<!-- What you expected to happen -->

## Actual Behavior
<!-- What actually happened — paste full terminal output below -->

```
paste output here
```

## Environment

| Field | Value |
|---|---|
| MiFlasher version | `miflasher --version` |
| Device model | e.g. Redmi Note 12 Pro |
| Device codename | e.g. ruby |
| Android version | e.g. 13 |
| MIUI/HyperOS version | e.g. MIUI 14.0.6 |
| Termux version | from `termux-info` |
| Python version | `python3 --version` |
| ADB version | `adb version` |

## Additional Context
<!-- Any other relevant information — USB cable, OTG adapter, etc. -->
```

---

## .github/ISSUE_TEMPLATE/feature_request.md

```markdown
---
name: Feature Request
about: Suggest a new feature or improvement
title: '[FEAT] '
labels: enhancement
assignees: ''
---

## Problem Statement
<!-- What problem does this feature solve? Who experiences it? -->

## Proposed Solution
<!-- Describe the feature. Include example CLI flags or GUI elements if applicable -->

**Example usage:**
```bash
miflasher [new-command] [--new-flag]
```

## Alternatives Considered
<!-- Have you tried any workarounds? Are there other tools that do this? -->

## Additional Context
<!-- Screenshots, mockups, links to similar features in other tools -->

## Are you willing to implement this?
- [ ] Yes, I can submit a PR
- [ ] No, but I can help test it
- [ ] No
```

---

## .github/ISSUE_TEMPLATE/compatibility.md

```markdown
---
name: Compatibility Report
about: Report a device that works or doesn't work with MiFlasher
title: '[COMPAT] Device: '
labels: compatibility
assignees: ''
---

## Device Information

| Field | Value |
|---|---|
| Device name | e.g. Redmi Note 12 Pro |
| Codename | e.g. ruby (Settings > About Phone > All Specs) |
| Chipset | e.g. Snapdragon 778G |
| Android version | |
| MIUI/HyperOS version | |
| Region variant | e.g. Global, China, India |

## Test Results

| Command | Result | Notes |
|---|---|---|
| `miflasher device` | ✅ / ⚠️ / ❌ | |
| `miflasher unlock` | ✅ / ⚠️ / ❌ | |
| `miflasher flash boot` | ✅ / ⚠️ / ❌ | |
| `miflasher flash rom` | ✅ / ⚠️ / ❌ | |
| `miflasher backup` | ✅ / ⚠️ / ❌ | |
| `miflasher restore` | ✅ / ⚠️ / ❌ | |
| `miflasher wipe` | ✅ / ⚠️ / ❌ | |
| `miflasher gui` | ✅ / ⚠️ / ❌ | |

## Issues Encountered
<!-- Describe any errors, unexpected behavior, or workarounds needed -->

## Full Output (for failures)
```
paste output here
```
```

---

## .github/PULL_REQUEST_TEMPLATE.md

```markdown
## Summary
<!-- What does this PR do? Be specific. -->

## Motivation
<!-- Why is this change needed? Link to related issue if any -->

Closes #

## Changes Made
<!-- List the files changed and what was done -->

- `core/xxx.py` — 
- `modules/xxx.py` — 

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that changes existing behavior)
- [ ] Documentation update
- [ ] Refactor (no functional changes)

## Testing
<!-- How did you test this? On what device? -->

**Device tested on:** [e.g. Redmi Note 12 Pro (ruby), MIUI 14.0.6]

**Commands tested:**
- [ ] `miflasher device`
- [ ] `miflasher flash ...`
- [ ] `miflasher unlock`
- [ ] `miflasher backup`
- [ ] `miflasher wipe`
- [ ] `miflasher gui`
- [ ] `miflasher config`

**Edge cases covered:**
- [ ] No device connected
- [ ] Invalid file/path input
- [ ] Ctrl+C interrupt
- [ ] Network failure (if applicable)

## Screenshots / Output
<!-- Paste terminal output or screenshots showing the feature works -->

```
paste output here
```

## Checklist
- [ ] My code follows the project's coding standards (see CONTRIBUTING.md)
- [ ] I've added type hints to all new functions
- [ ] I've added docstrings to all public methods
- [ ] I'm not using bare `print()` in core modules (using `self.log` instead)
- [ ] Error handling covers edge cases
- [ ] Commit messages follow conventional commits format
- [ ] I've tested on a real device (or clearly documented I haven't)
- [ ] I've updated documentation if needed
```
