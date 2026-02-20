# ⚡ MiFlasher 

> **Advanced Xiaomi Flash & Unlock Toolkit for Termux**

A professional-grade command-line and web GUI toolkit for flashing, unlocking, backing up, and managing Xiaomi devices — all from your Android phone via Termux.

---

## ✨ What's New 

| Feature | v1 | v2 |
|---|---|---|
| Flash targets | ROM, boot, payload | + vbmeta, recovery, super |
| Progress bar | Basic | Rich: speed, ETA, size |
| Download | Basic | Resumable, retry, checksum |
| Device info | Serial only | Full: RAM, storage, battery, slot, display... |
| Reboot modes | — | system, bootloader, recovery, fastbootd, EDL |
| Backup | — | ✅ All partitions + compress |
| Restore | — | ✅ Full restore from backup |
| Wipe | — | ✅ data, cache, dalvik |
| Logging | print() | Leveled, colored, file output, session history |
| GUI | Static file server | Full dashboard with device polling, real-time |
| Config | — | ✅ Persistent JSON config |
| Error handling | Bare except | Typed, informative, with recovery tips |
| CLI | Positional args | Full argparse with subcommands + `--help` |

---

## 📦 Installation

```bash
# Clone or download MiFlasher
cd ~/miflasher

# Run installer
bash install.sh

# Reload shell
source ~/.bashrc
```

---

## 🚀 Usage

```bash
# Show connected device info
miflasher device

# Watch for device connect/disconnect
miflasher device --watch

# Reboot to bootloader
miflasher device --reboot bootloader

# Unlock bootloader (guided)
miflasher unlock

# Flash full ROM (zip or tgz)
miflasher flash rom --path /sdcard/Download/miui_MARBLE_rom.zip
miflasher flash rom --url https://bigota.d.miui.com/...rom.tgz

# Flash boot image
miflasher flash boot --path boot.img

# Flash recovery
miflasher flash recovery --path recovery.img --slot a

# Flash payload.bin
miflasher flash payload --path payload.bin

# Backup all partitions
miflasher backup --all

# Backup specific partitions
miflasher backup --partition boot recovery vbmeta

# Restore backup
miflasher restore --path ~/storage/downloads/MiFlasher/backups/backup_20250101.tar.gz

# Wipe data + cache
miflasher wipe --data --cache

# View logs
miflasher logs
miflasher logs --list

# Web GUI dashboard
miflasher gui
miflasher gui --port 9090

# Configuration
miflasher config --show
miflasher config --set theme=dark auto_verify=true
```

---

## 🗂️ Project Structure

```
miflasher/
├── miflasher          # Main CLI entry point
├── install.sh         # Termux auto-installer
├── requirements.txt   # Python dependencies
├── core/
│   ├── banner.py      # ASCII art banner
│   ├── logger.py      # Rich colored logger + progress bar
│   ├── device.py      # ADB/Fastboot device detection + info
│   ├── flash.py       # Flash manager (ROM, boot, payload, etc.)
│   ├── downloader.py  # Resumable downloader with checksum
│   ├── unlock.py      # Bootloader unlock manager
│   ├── backup.py      # Partition backup & restore
│   ├── wipe.py        # Partition wipe manager
│   ├── config.py      # Persistent configuration
│   └── session.py     # Session log management
├── modules/
│   └── miunlock_wrapper.py  # Mi Unlock tool wrapper
└── gui/
    └── app.py         # Full web dashboard (single-file SPA)
```

---

## ⚙️ Requirements

- **Termux** (Android) with `pkg install python android-tools pv`
- USB OTG cable or ADB over WiFi
- For unlocking: Mi Account linked for 7+ days, Developer Options enabled

---

## 📋 Supported Operations

| Command | Description |
|---|---|
| `device` | Full device info, reboot modes, watch mode |
| `unlock` | Bootloader unlock via miunlock + fastboot fallback |
| `flash rom` | Flash full ROM (ZIP/TGZ), auto-runs flash script |
| `flash boot` | Flash boot.img with A/B slot support |
| `flash recovery` | Flash recovery image |
| `flash vbmeta` | Flash vbmeta (required for Magisk) |
| `flash payload` | Flash OTA via payload.bin |
| `flash super` | Flash super/dynamic partition |
| `backup` | Backup partitions via fastboot fetch or adb pull |
| `restore` | Restore partitions from backup directory/archive |
| `wipe` | Wipe data, cache, dalvik-cache |
| `logs` | View, search, clear session logs |
| `gui` | Full web dashboard at localhost:8080 |
| `config` | Persistent settings management |

---

## 🔒 Safety Features

- **Confirmation prompts** on destructive operations (wipe, unlock, restore)
- **Checksum verification** on downloads (SHA256/MD5)
- **Resumable downloads** — interrupted downloads continue
- **Mode detection** — warns if device not in correct mode (ADB vs Fastboot)
- **Pre-flash validation** — checks file existence and format
- **Structured logging** — every session logged to `~/.local/share/miflasher/logs/`

---

## 📜 License

MIT License — free to use, modify, and distribute.
