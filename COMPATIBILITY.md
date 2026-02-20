# Device Compatibility

This document tracks known-working and known-problematic devices.

> **Help wanted!** If you've tested MiFlasher on a device not listed here, please open a [Compatibility Report](https://github.com/yourusername/miflasher/issues/new?template=compatibility.md) issue.

---

## Legend

| Symbol | Meaning |
|---|---|
| ✅ | Fully working |
| ⚠️ | Mostly working, see notes |
| ❌ | Not working |
| 🔄 | Untested / unknown |
| 🔒 | Bootloader cannot be unlocked (carrier-locked, etc.) |

---

## Tested Devices

### Redmi Series

| Device | Codename | Android | MIUI | device | unlock | flash | backup | Notes |
|---|---|---|---|---|---|---|---|---|
| Redmi Note 12 Pro | ruby | 13 | 14.0.6 | ✅ | ✅ | ✅ | ✅ | A/B device |
| Redmi Note 11 | spes | 12 | 13.0.9 | ✅ | ✅ | ✅ | ⚠️ | backup needs root for some partitions |
| Redmi Note 10 Pro | sweetin | 11 | 12.5 | ✅ | ✅ | ✅ | ✅ | |
| Redmi 9 | lancelot | 10 | 12.0.3 | ✅ | ✅ | ⚠️ | ✅ | payload flash not supported |
| Redmi 9A | dandelion | 10 | 12.0.1 | ✅ | ✅ | ✅ | ✅ | A-only device |

### Xiaomi Series

| Device | Codename | Android | MIUI | device | unlock | flash | backup | Notes |
|---|---|---|---|---|---|---|---|---|
| Xiaomi 12 | cupid | 12 | 13.0 | ✅ | ✅ | ✅ | ✅ | A/B device, VAB |
| Xiaomi 11T | agate | 11 | 12.5 | ✅ | ✅ | ✅ | ⚠️ | |
| Xiaomi Mi 9 | cepheus | 10 | 12.0.1 | ✅ | ✅ | ✅ | ✅ | |

### POCO Series

| Device | Codename | Android | MIUI | device | unlock | flash | backup | Notes |
|---|---|---|---|---|---|---|---|---|
| POCO X5 Pro | redwood | 12 | 14.0.5 | ✅ | ✅ | ✅ | ✅ | |
| POCO F4 | munch | 12 | 13.0.6 | ✅ | ✅ | ✅ | ✅ | A/B device |
| POCO M4 Pro | fleur | 11 | 13.0.2 | ✅ | ✅ | ✅ | ✅ | |

---

## Known Issues by Feature

### `miflasher device`
- **A-only devices:** Slot shows `N/A (A-only)` — expected behavior
- **EDL mode:** Device not detectable via ADB/Fastboot in EDL; shows nothing
- **Unauthorized ADB:** Shows `USB-UNKNOWN` — accept the prompt on device screen

### `miflasher unlock`
- **7-day waiting period:** Xiaomi requires devices to be linked for 7 days before unlock
- **Carrier-locked devices:** Some carrier variants cannot be unlocked
- **HyperOS (MIUI 14+):** Flow is the same, same URL format

### `miflasher flash`
- **VAB (Virtual A/B) devices:** Super partition flash works differently — use `flash super` not individual partition images
- **Fastboot mode required:** All flash operations require device in Fastboot/Fastbootd mode
- **payload.bin:** Requires `payload-dumper-go` or `payload_dumper` to be installed separately

### `miflasher backup`
- **Root required for some partitions:** `persist`, `modem`, `bluetooth` may be inaccessible without root
- **super partition:** Very large (10–20 GB), ensure enough storage before backing up

---

## Untested Configurations

The following have not been tested and may or may not work:

- Xiaomi devices sold in China with locked `persist` partitions
- Devices with HyperOS 2.0+ (released 2025)
- MediaTek (MTK) chipset devices — mostly Fastboot is limited on MTK
- Devices in EDL (Emergency Download) mode — requires specialized tools (edl.py, QFIL)
- Devices with FRP (Factory Reset Protection) lock

---

## Chipset Notes

### Qualcomm (Snapdragon)
Full support. ADB and Fastboot work normally. EDL mode available on most devices.

### MediaTek (Helio/Dimensity)
Partial support. ADB works normally. Fastboot is more limited:
- `fastboot erase` may not work on all partitions
- Some partitions are not flashable via stock Fastboot
- Consider SP Flash Tool for deeper MTK operations

---

## How to Report Compatibility

Open a [Compatibility Report issue](https://github.com/djunekz/miflasher/issues/new) with:

```
Device: [name]
Codename: [codename from Settings > About Phone > All Specs]
Chipset: [e.g. Snapdragon 778G]
Android version: [e.g. 13]
MIUI/HyperOS version: [e.g. MIUI 14.0.6]
Termux version: [from: termux-info | grep version]

Commands tested:
- miflasher device    : [✅ / ⚠️ / ❌] — notes
- miflasher unlock    : [✅ / ⚠️ / ❌] — notes
- miflasher flash boot: [✅ / ⚠️ / ❌] — notes
- miflasher backup    : [✅ / ⚠️ / ❌] — notes

Any errors or unexpected behavior:
[paste output]
```
