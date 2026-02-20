# Troubleshooting Guide

Solutions to the most common issues with MiFlasher.

---

## Quick Diagnostics

Run this first to gather info for any issue:

```bash
# Check MiFlasher version
./miflasher --version

# Check dependencies
which adb && adb version
which fastboot && fastboot --version
python3 --version

# Check device connection
adb devices
fastboot devices

# Check verbose output
./miflasher device --verbose
```

---

## Device Detection Issues

### "No device detected" / "USB-UNKNOWN"

**Symptoms:**
```
[ERROR] No device detected. Check USB cable & USB Debugging.
```
or
```
| Mode | USB-UNKNOWN |
```

**Causes and fixes:**

**1. USB Debugging not enabled**
```
Settings → About Phone → tap "MIUI Version" 7 times
→ Settings → Additional Settings → Developer Options
→ Enable USB Debugging
```

**2. Device showing "Unauthorized" in ADB**
```bash
adb devices
# Shows: XXXXXXXX  unauthorized
```
→ On your device screen: tap **"Allow USB Debugging"** → check "Always allow from this computer" → tap OK

**3. ADB server needs restart**
```bash
adb kill-server
adb start-server
adb devices
```

**4. Wrong USB mode**
When connecting via USB, select **"File Transfer (MTP)"** — not "Charging only"

**5. Cable/adapter issue**
- Try a different USB cable (data cable, not charge-only)
- Try a different USB OTG adapter
- Try direct USB-C to USB-C if both devices support it

**6. ADB over WiFi (if USB doesn't work)**
```bash
# On device: Settings → Developer Options → Wireless Debugging → Enable
# Note the IP and port shown
adb connect 192.168.1.x:5555
./miflasher device
```

---

### Device shows but mode is wrong

**Device in ADB but you need Fastboot:**
```bash
miflasher device --reboot bootloader
# OR
adb reboot bootloader
```

**Device in Fastboot but you need ADB:**
```bash
fastboot reboot
# Wait for boot, then reconnect
```

---

## Flash Issues

### "No device in fastboot mode"

```
[ERROR] No device detected in fastboot mode.
```

Fix:
1. Power off device completely
2. Hold **Volume Down + Power** simultaneously for 8–10 seconds
3. Release when you see the Fastboot/Mi Bunny screen
4. Connect USB cable
5. Verify: `fastboot devices`
6. Retry flash

### "FAILED (remote: 'partition not found')"

The partition name doesn't exist on your device. Common causes:

- **A/B device** — try with slot suffix: `fastboot flash boot_a boot.img`
- **Partition name mismatch** — check your device's partition layout
- **Wrong ROM** — you may be flashing a ROM for a different device

### "FAILED (remote: 'not allowed in locked state')"

Bootloader is locked. You must unlock it first:
```bash
miflasher unlock
```

### ROM flash completes but device won't boot

1. Boot to recovery (Vol+ + Power)
2. Wipe cache and dalvik: `miflasher wipe --cache --dalvik`
3. If still stuck: try factory reset
4. If still stuck: flash a known-good ROM

### "payload-dumper-go not found"

```bash
# Install payload-dumper-go
pip install payload-dumper-go --break-system-packages
# OR
pkg install payload-dumper-go
```

---

## Unlock Issues

### "Could not extract token from URL"

Old issue — fixed in v2.0.0. Update to latest version.

If still happening: paste the **complete URL** from browser address bar, including `https://` and all parameters after `?`.

Example of a valid URL:
```
https://unlock.update.miui.com/sts?d=wb_33715c01-c3a2-415e-9b2b-f3567aba9de7&ticket=0&auth=xxx...
```

### "Account check failed: Expecting value"

This is expected — Xiaomi's unlock API requires proprietary signing that can't be replicated. MiFlasher still validates your login and gives you the fastboot next steps. This is not an error that blocks you.

### "fastboot flashing unlock" rejected

```
FAILED (remote: 'Flashing Unlock is not allowed')
```

Causes:
1. **OEM Unlocking not enabled** → Settings → Developer Options → OEM Unlocking → Enable
2. **Waiting period not complete** → Check "Mi Unlock Status" in Developer Options
3. **Device region restriction** → Some regional variants cannot be unlocked

### "Bootloader unlock failed" / device stuck

1. Reboot device: hold Power for 10+ seconds
2. If device is stuck in a bootloop after unlock attempt, boot to recovery (Vol+ + Power)
3. In recovery, do a factory reset
4. If no recovery access, try EDL mode (device-specific steps)

---

## Download Issues

### Download is slow or keeps failing

```bash
# Check network
ping -c 3 8.8.8.8

# Check if URL is valid
curl -I "YOUR_ROM_URL"
```

MiFlasher automatically resumes interrupted downloads — just run the same command again.

### "Checksum MISMATCH"

The downloaded file is corrupt or the wrong file.

1. Delete the partial/corrupt file
2. Verify the checksum value from the ROM provider
3. Try a different mirror URL
4. Re-run download

---

## Backup Issues

### "Could not backup: persist" or other partitions

Some partitions require root:
```bash
# Check if you have root
su -c "ls /dev/block/by-name/persist"
```

Without root, only partitions accessible via `fastboot fetch` can be backed up. This is a Xiaomi/Android limitation, not a MiFlasher bug.

### Backup takes forever

The `super` partition can be 10–20 GB. This is expected. Ensure you have enough storage:
```bash
df -h ~/storage/downloads/
```

### "No .img files found in backup"

Your backup directory is empty or contains no `.img` files. The backup may have failed silently. Check logs:
```bash
miflasher logs --tail 100
```

---

## GUI Issues

### Can't open localhost:8080 in browser

```bash
# Check if GUI is running
ps aux | grep miflasher

# Check if port is in use
netstat -tlnp | grep 8080

# Try different port
miflasher gui --port 9090
```

### Device info not updating in GUI

The GUI polls every 5 seconds. If device disconnects and reconnects, wait up to 5 seconds. If still not updating, refresh the page.

### GUI accessible from other devices (I don't want this)

By default the GUI only binds to `localhost`. If you've used `--host 0.0.0.0`, stop and restart without that flag:
```bash
# Kill existing instance
pkill -f "miflasher gui"

# Restart safely (localhost only)
miflasher gui
```

---

## Installation Issues

### `./miflasher: Permission denied`

```bash
chmod +x miflasher
./miflasher --help
```

### `ModuleNotFoundError: No module named 'requests'`

```bash
pip install requests --break-system-packages
```

### `adb: command not found` / `fastboot: command not found`

```bash
pkg install android-tools
```

### `SyntaxError` or `IndentationError` on startup

You may have a corrupt file. Re-download the file from GitHub:
```bash
git fetch origin
git checkout origin/master -- miflasher
```

Or re-clone the repo:
```bash
cd ..
rm -rf miflasher
git clone https://github.com/djunekz/miflasher
```

---

## Getting More Help

If none of the above fixes your issue:

1. **Enable verbose mode** and copy the full output:
   ```bash
   ./miflasher device --verbose
   ./miflasher flash boot --path boot.img --verbose
   ```

2. **Check existing issues** on GitHub — someone may have had the same problem

3. **Open a new issue** with:
   - Your device model and MIUI version
   - Exact command you ran
   - Full terminal output (with `--verbose`)
   - MiFlasher version (`./miflasher --version`)

We're here to help. Don't give up!
