# Changelog

All notable changes to MiFlasher are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- ADB WiFi pairing support (`miflasher device --pair`)
- ROM search/browse from known Xiaomi mirrors
- Automated Magisk patching workflow
- Interactive TUI mode (curses)
- Plugin system for custom modules

---

## [2.0.0] — 2026-02-20

Major rewrite. Everything improved.

### Added
- **Full argparse CLI** with subcommands, `--help`, and `--version`
- **`miflasher device`** — full device info table (RAM, storage, battery, display, security patch, slot, kernel)
- **`miflasher device --watch`** — real-time device connection monitoring
- **`miflasher device --reboot <mode>`** — reboot to system / bootloader / recovery / fastbootd / EDL
- **`miflasher device --json`** — JSON output for scripting
- **`miflasher flash recovery`** — flash recovery images
- **`miflasher flash vbmeta`** — flash vbmeta (required for Magisk on some devices)
- **`miflasher flash super`** — flash super / dynamic partition images
- **`miflasher flash payload`** — flash OTA packages via `payload.bin`
- **A/B slot support** — `--slot a`, `--slot b`, `--slot all`
- **`miflasher backup`** — backup all or specific partitions via `fastboot fetch` + ADB fallback
- **`miflasher backup --compress`** — compress backup to `.tar.gz`
- **`miflasher restore`** — restore from backup directory or archive
- **`miflasher wipe`** — wipe data / cache / dalvik-cache partitions
- **`miflasher logs`** — view, tail, list, and clear session logs
- **`miflasher config`** — persistent JSON configuration with get/set/show/reset
- **Rich logger** — leveled logging (DEBUG/INFO/SUCCESS/WARNING/ERROR/CRITICAL), colored output, icons, tables, progress bar with speed/ETA, confirmation prompts
- **Resumable downloader** — continues interrupted downloads, retry on failure, SHA256/MD5 verification
- **Mi Account browser login flow** — no Windows PC needed for authentication step
- **STS redirect URL parser** — handles real Xiaomi `?d=wb_xxx&auth=xxx&nonce=xxx` format
- **Web GUI** — full single-page dashboard with device info polling, flash/wipe/backup panels, log viewer, dark theme
- **Session logging** — every session saved as JSONL to `~/.local/share/miflasher/logs/`
- **`install.sh`** — one-command Termux installer
- **Clean Ctrl+C handling** — no more tracebacks on interrupt

### Changed
- **Complete rewrite** from ~100 lines to 2,500+ lines across 13 files
- `miflasher device` now shows 16 properties instead of just serial number
- `miflasher unlock` no longer requires USB for Mi Account authentication
- `miflasher flash rom` now auto-runs flash scripts OR falls back to manual image flashing
- GUI is now a real web app (not just a static file server)
- Logger replaces all bare `print()` calls

### Fixed
- Duplicate `rom` subparser causing `argparse.ArgumentError` on startup
- `ValueError: not enough values to unpack` in `_prompt_login()` on Ctrl+C
- `SyntaxError: unterminated string literal` from embedded ANSI bytes in source
- `USB-UNKNOWN` detection ordering (ADB/Fastboot checked before termux-usb)
- STS redirect URL parsing failing on real Xiaomi `?d=` format (was only looking for `?token=`)

### Removed
- Dependency on external `miunlock` binary (now handled internally)
- `core/payload.py` (merged into `core/flash.py`)
- `core/utils.py` (merged into `core/logger.py` and individual modules)

---

## [1.0.0] — 2024-01-15

Initial release.

### Added
- `miflasher device` — basic ADB/Fastboot device detection
- `miflasher unlock` — wrapper around external `miunlock` binary
- `miflasher flash-rom <path>` — decompress and flash ROM
- `miflasher flash-boot <boot.img>` — flash boot image via fastboot
- `miflasher flash-payload <payload.bin>` — flash payload via payload_dumper
- `miflasher gui` — minimal static file server on localhost:8080
- Basic colored logger
- `install.sh` installer

---

## Version Scheme

`MAJOR.MINOR.PATCH`

- **MAJOR** — breaking changes to CLI interface or behavior
- **MINOR** — new features, new commands, significant improvements
- **PATCH** — bug fixes, minor improvements, documentation

---

[Unreleased]: https://github.com/djunekz/miflasher/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/djunekz/miflasher/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/djunekz/miflasher/releases/tag/v1.0.0
