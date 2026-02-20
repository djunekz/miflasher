<div align="center">

```md

     ░█▄█░▀█▀░█▀▀░█░░░█▀█░█▀▀░█░█░█▀▀░█▀▄
     ░█░█░░█░░█▀▀░█░░░█▀█░▀▀█░█▀█░█▀▀░█▀▄
     ░▀░▀░▀▀▀░▀░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀

```

**Advanced Xiaomi Flash & Unlock Toolkit**

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg?style=flat-square)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Termux-orange.svg?style=flat-square)](https://termux.dev)
[![Version](https://img.shields.io/badge/version-2.0.0-purple.svg?style=flat-square)](CHANGELOG.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

*Flash ROMs, unlock bootloaders, backup partitions — all from your phone.*

[Getting Started](#-installation) · [Commands](#-commands) · [Features](#-features) · [FAQ](#-faq) · [Contributing](CONTRIBUTING.md)

</div>

---

## 📖 Overvieww

MiFlasher is a **fully open-source** command-line toolkit and web GUI for managing Xiaomi/MIUI devices from [Termux](https://termux.dev) on Android. No PC required for most operations.

Built for power users, developers, and ROM flashers who want a professional, scriptable tool — not a bloated Windows-only GUI.


Example:
```
$ ./miflasher device

  Device Information
  +-----------------+--------------------------------+
  | Property        | Value                          |
  +-----------------+--------------------------------+
  | Serial          | 1a2b3c4d                       |
  | Mode            | ADB                            |
  | Brand           | Xiaomi                         |
  | Model           | Redmi Note 12 Pro              |
  | Codename        | ruby                           |
  | Android Version | 13                             |
  | MIUI Version    | MIUI 14.0.6                    |
  | RAM             | 5824 MB free / 8192 MB total   |
  | Bootloader      | yes (unlocked)                 |
  | Battery         | 87% (Charging)                 |
  +-----------------+--------------------------------+
```

---

## ✨ Features

### 🔧 Device Management
- Full device info: model, RAM, storage, battery, display, security patch, slot, kernel
- Real-time device watch mode (`--watch`)
- Reboot to any mode: System, Bootloader, Recovery, Fastbootd, EDL

### ⚡ Flashing
- Flash full ROM packages (ZIP / TGZ / TAR.GZ)
- Flash individual images: boot, recovery, vbmeta, super
- Flash OTA packages via `payload.bin`
- A/B slot support (flash to slot A, B, or both)
- Auto-detect and run Xiaomi flash scripts (`flash_all.sh`, etc.)

### 🔓 Bootloader Unlock
- Browser-based Mi Account login flow (no PC needed)
- Session token extraction from redirect URL
- Guided step-by-step unlock instructions
- Direct fastboot unlock (`--fastboot-only`) for already-authorized devices

### 💾 Backup & Restore
- Backup any/all partitions via `fastboot fetch` or ADB
- Optional GZIP compression of backup archives
- Full restore from backup directory or `.tar.gz`
- Smart per-partition status reporting

### 🌐 Web GUI
- Full single-page dashboard at `http://localhost:8080`
- Real-time device polling (auto-refreshes every 5s)
- Flash, wipe, backup, unlock — all from browser
- Session log viewer
- Dark theme, responsive layout

### 📋 Logging & Sessions
- Leveled colored logging: DEBUG / INFO / SUCCESS / WARNING / ERROR / CRITICAL
- Every session saved to `~/.local/share/miflasher/logs/` as JSONL
- View, tail, filter, and clear logs via `miflasher logs`

### ⚙️ Configuration
- Persistent JSON config at `~/.config/miflasher/config.json`
- Set download dir, backup dir, auto-verify, GUI port, and more
- Per-command overrides via flags

---

## 📋 Requirements if run Android/Termux

| Requirement | Notes |
|---|---|
| **Android** | 9+ (API 28+) |
| **Termux** | Latest from [F-Droid](https://f-droid.org/packages/com.termux/) recommended |
| **Python** | 3.10 or newer |
| **android-tools** | Provides `adb` and `fastboot` |
| **USB OTG** | For ADB/Fastboot device connection |
| **Mi Account** | For bootloader unlock authorization |

> ⚠️ **Note:** Do NOT install Termux from the Play Store — use F-Droid for the latest version.

---

## 🚀 Installation

### Quick Install (Recommended)

```bash
# 1. Clone the repo
git clone https://github.com/djunekz/miflasher
cd miflasher

# 2. Run installer
bash install.sh

# 3. Reload shell
source ~/.bashrc

# 4. Test
miflasher --version
```

### Manual Install

```bash
# Install system dependencies
pkg update && pkg install python android-tools pv

# Install Python dependencies
pip install requests --break-system-packages

# Make executable and symlink
chmod +x miflasher
ln -sf "$(pwd)/miflasher" ~/.local/bin/miflasher

# Grant storage access
termux-setup-storage
```

### Verify Installation

```bash
miflasher --version

miflasher --help
```

---

## 📚 Commands

### `miflasher device`
```bash
miflasher device                    # Show device info table
miflasher device --watch            # Live device monitor
miflasher device --json             # Output as JSON (for scripting)
miflasher device --reboot bootloader  # Reboot to specific mode
```
Reboot modes: `system` `bootloader` `recovery` `fastbootd` `edl`

---

### `miflasher unlock`
```bash
miflasher unlock                    # Mi Account login + guided unlock
miflasher unlock --force            # Skip confirmation prompt
miflasher unlock --fastboot-only    # Direct fastboot unlock (USB required)
miflasher unlock --token TOKEN      # Use pre-obtained token
```

**Unlock flow:**
1. Tool displays Mi Account login URL
2. Log in via your phone browser
3. Browser redirects → copy the URL from address bar
4. Paste into terminal → tool verifies session
5. Follow the displayed fastboot instructions

---

### `miflasher flash`
```bash
# ROM (auto-runs flash_all.sh or flashes all .img files)
miflasher flash rom --path /sdcard/Download/miui_rom.zip
miflasher flash rom --url https://bigota.d.miui.com/.../miui_rom.tgz
miflasher flash rom --path rom.zip --keep-data   # Preserve /data

# Boot image (Magisk, patched boot, etc.)
miflasher flash boot --path boot.img
miflasher flash boot --path boot.img --slot a    # Flash to slot A only

# Other images
miflasher flash recovery --path recovery.img
miflasher flash vbmeta   --path vbmeta.img
miflasher flash super    --path super.img
miflasher flash payload  --path payload.bin

# Shared flags
--slot [a|b|all]      # Target slot (default: all)
--skip-verify         # Skip checksum verification
--no-reboot           # Do not reboot after flash
--wipe-data           # Wipe /data after flash
```

---

### `miflasher backup`
```bash
miflasher backup --all                          # Backup all known partitions
miflasher backup --partition boot recovery      # Backup specific partitions
miflasher backup --all --compress               # Compress to .tar.gz
miflasher backup --all --out /sdcard/mybackups  # Custom output directory
```

### `miflasher restore`
```bash
miflasher restore --path /sdcard/MiFlasher/backups/backup_20250101
miflasher restore --path backup.tar.gz
miflasher restore --path backup/ --partition boot vbmeta  # Selective restore
```

### `miflasher wipe`
```bash
miflasher wipe --data             # Wipe /data (factory reset)
miflasher wipe --cache            # Wipe cache partition
miflasher wipe --dalvik           # Wipe Dalvik/ART cache
miflasher wipe --all              # Wipe data + cache + dalvik
miflasher wipe --all --force      # Skip confirmation
```

---

### `miflasher logs`
```bash
miflasher logs                    # Show last 50 log lines
miflasher logs --tail 100         # Show last 100 lines
miflasher logs --list             # List all saved sessions
miflasher logs --session 20250101_130000  # View specific session
miflasher logs --clear            # Delete all logs
```

### `miflasher gui`
```bash
miflasher gui                     # Start at http://localhost:8080
miflasher gui --port 9090         # Custom port
miflasher gui --no-browser        # Don't auto-open browser
miflasher gui --host 0.0.0.0      # Accessible from other devices on network
```

### `miflasher config`
```bash
miflasher config --show           # Show all config values
miflasher config --get theme      # Get single value
miflasher config --set theme=dark auto_verify=true
miflasher config --reset          # Reset to defaults
```

---

## 🗂️ Project Structure

```
miflasher/
├── miflasher              # Main CLI entry point (executable)
├── install.sh             # Termux auto-installer
├── requirements.txt       # Python dependencies
│
├── core/                  # Core modules
│   ├── banner.py          # ASCII art banner
│   ├── logger.py          # Rich colored logger, progress bar, tables
│   ├── device.py          # ADB/Fastboot device detection & info
│   ├── flash.py           # Flash manager (ROM, boot, payload, etc.)
│   ├── downloader.py      # Resumable downloader with checksum verify
│   ├── unlock.py          # Bootloader unlock manager
│   ├── backup.py          # Partition backup & restore
│   ├── wipe.py            # Partition wipe manager
│   ├── config.py          # Persistent configuration
│   └── session.py         # Session log management
│
├── modules/               # Plugin-style modules
│   └── miunlock_wrapper.py  # Mi Account unlock flow
│
├── gui/                   # Web dashboard
│   └── app.py             # Single-file SPA (HTML + CSS + JS + API)
│
 Documentation
 ├── README.md
 ├── CONTRIBUTING.md
 ├── SECURITY.md
 └── CODE_OF_CONDUCT.md and etc docs
```

---

## ⚙️ Configuration Reference

Config file: `~/.config/miflasher/config.json`

| Key | Default | Description |
|---|---|---|
| `theme` | `dark` | CLI/GUI theme |
| `download_dir` | `~/storage/downloads/MiFlasher` | ROM download directory |
| `backup_dir` | `~/storage/downloads/MiFlasher/backups` | Partition backup directory |
| `log_dir` | `~/.local/share/miflasher/logs` | Session log directory |
| `auto_verify` | `true` | Auto checksum-verify downloads |
| `auto_reboot` | `true` | Auto-reboot device after flash |
| `slot` | `all` | Default flash slot (a/b/all) |
| `gui_port` | `8080` | Web GUI port |
| `gui_host` | `localhost` | Web GUI host |
| `verbose` | `false` | Enable debug logging |

---

## ❓ FAQ

<details>
<summary><b>Do I need root to use MiFlasher?</b></summary>

No. MiFlasher uses standard `adb` and `fastboot` — no root required. Some features (like reading `/dev/block/` partitions for backup) may work better with root, but it is never required.

</details>

<details>
<summary><b>Why does <code>miflasher device</code> show "USB-UNKNOWN"?</b></summary>

This means `termux-usb` detected a USB device, but ADB and Fastboot didn't respond. Common causes:

1. USB Debugging not enabled → Settings → Developer Options → USB Debugging
2. ADB server not running → `adb kill-server && adb start-server`
3. Device shows "Unauthorized" → tap Allow on device screen
4. Wrong USB mode → use "File Transfer" (MTP) mode, not "Charging only"

</details>

<details>
<summary><b>Can I unlock the bootloader without a Windows PC?</b></summary>

Partially. MiFlasher handles the Mi Account authentication entirely from your phone (browser login). However, the final fastboot unlock step still requires a USB connection to execute `fastboot flashing unlock`. You do NOT need a separate PC — you can use `miflasher unlock --fastboot-only` from Termux itself.

</details>

<details>
<summary><b>Why does the Xiaomi unlock API return empty responses?</b></summary>

Xiaomi's unlock API (`unlock.update.miui.com`) uses proprietary HMAC signatures generated by their official Windows tool using a hardcoded secret key. This key is not publicly available, so direct API calls cannot be properly signed and the server returns empty/error responses. MiFlasher handles everything that can be done without that key.

</details>

<details>
<summary><b>My device is A/B (VAB). How do slots work?</b></summary>

A/B devices have two copies of partitions (slot_a and slot_b). MiFlasher defaults to flashing both (`--slot all`). If you want to flash to a specific slot only, use `--slot a` or `--slot b`. After flashing, the device boots from the updated slot.

</details>

<details>
<summary><b>Flash failed with "No device in fastboot mode". What do I do?</b></summary>

1. Make sure device is in fastboot mode: hold **Vol- + Power** for ~10 seconds until Fastboot screen appears
2. Connect USB cable
3. Run `fastboot devices` — device should appear
4. Retry: `miflasher flash boot --path boot.img`

If `fastboot devices` is empty even with device showing Fastboot screen, try a different USB cable or USB OTG adapter.

</details>

<details>
<summary><b>How do I flash Magisk?</b></summary>

1. Download Magisk APK from [Magisk releases](https://github.com/topjohnwu/Magisk/releases)
2. In Magisk app: Install → Select and Patch a File → pick your `boot.img`
3. Magisk saves `magisk_patched_XXXXX.img` to `/sdcard/Download/`
4. Flash it: `miflasher flash boot --path /sdcard/Download/magisk_patched_XXXXX.img`
5. Reboot: `miflasher device --reboot system`

</details>

---

## 🛡️ Safety & Disclaimers

> **USE AT YOUR OWN RISK.**

- Flashing incorrect ROMs or images can **brick your device**
- Bootloader unlock **permanently wipes all user data**
- Always **backup important data** before any flash/unlock operation
- Verify ROM checksums before flashing
- This tool is provided as-is, without warranty of any kind

See [SECURITY.md](SECURITY.md) for vulnerability reporting and [LICENSE](LICENSE) for full terms.

---

## 🤝 Contributingg

We welcome contributions of all kinds — bug fixes, new features, documentation improvements, and translations.

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to set up a development environment
- Coding standards and style guide
- How to submit pull requests
- Issue reporting guidelines

---

## 📄 License

MIT License

Full license: [LICENSE](LICENSE)

---

## 🙏 Acknowledgements

- [Termux](https://termux.dev) — the Android terminal that makes this possible
- [android-tools](https://developer.android.com/tools/adb) — ADB and Fastboot
- [miunlock](https://github.com/some/miunlock) — original Mi unlock inspiration
- [Magisk](https://github.com/topjohnwu/Magisk) — root solution for Xiaomi devices
- All contributors and testers in the community

---

<div align="center">

Made with love for the Android modding community

**[⭐ Star this repo](https://github.com/djunekz/miflasher)** if MiFlasher helped you!

</div>
