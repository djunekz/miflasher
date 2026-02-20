#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
#  MiFlasher v2.0 — Termux Installer
# =============================================================================

set -e

CYAN="\033[1;36m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
DIM="\033[2m"
RESET="\033[0m"

echo -e "${CYAN}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║       MiFlasher v2.0 Installer          ║"
echo "  ║     Advanced Xiaomi Flash Toolkit        ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${RESET}"

step() { echo -e "\n${CYAN}▶ $1${RESET}"; }
ok()   { echo -e "${GREEN}  ✓ $1${RESET}"; }
warn() { echo -e "${YELLOW}  ⚠ $1${RESET}"; }
fail() { echo -e "${RED}  ✗ $1${RESET}"; exit 1; }

# ── 1. Packages ──────────────────────────────────────────────────────────────
step "Installing system packages..."
pkg update -y -q
pkg install -y -q python android-tools pv curl wget tar gzip 2>/dev/null || warn "Some packages may have failed"
ok "System packages"

# ── 2. Storage permission ─────────────────────────────────────────────────────
step "Requesting storage permission..."
if [ ! -d ~/storage ]; then
  termux-setup-storage && ok "Storage access granted" || warn "Storage permission not granted"
else
  ok "Storage already accessible"
fi
mkdir -p ~/storage/downloads/MiFlasher
mkdir -p ~/storage/downloads/MiFlasher/backups

# ── 3. Python deps ───────────────────────────────────────────────────────────
step "Installing Python packages..."
pip install requests colorama --break-system-packages -q || warn "pip install had issues"
ok "Python packages"

# Optional packages (best-effort)
pip install miunlock --break-system-packages -q 2>/dev/null && ok "miunlock" || warn "miunlock unavailable (optional)"

# ── 4. Install miflasher ─────────────────────────────────────────────────────
step "Installing MiFlasher..."
INSTALL_DIR="$HOME/.local/lib/miflasher"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# Copy files
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true

# Create __init__.py for all packages
touch "$INSTALL_DIR/core/__init__.py"
touch "$INSTALL_DIR/modules/__init__.py"
touch "$INSTALL_DIR/gui/__init__.py"

# Create launcher
cat > "$BIN_DIR/miflasher" << LAUNCHER
#!/data/data/com.termux/files/usr/bin/bash
cd "$INSTALL_DIR"
python3 miflasher "\$@"
LAUNCHER
chmod +x "$BIN_DIR/miflasher"
ok "Launcher: $BIN_DIR/miflasher"

# ── 5. PATH ───────────────────────────────────────────────────────────────────
step "Configuring PATH..."
SHELL_RC="$HOME/.bashrc"
if ! grep -q '.local/bin' "$SHELL_RC" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
  ok "Added ~/.local/bin to PATH in .bashrc"
else
  ok "PATH already configured"
fi
export PATH="$HOME/.local/bin:$PATH"

# ── 6. Config dir ─────────────────────────────────────────────────────────────
step "Creating config directory..."
mkdir -p "$HOME/.config/miflasher"
mkdir -p "$HOME/.local/share/miflasher/logs"
ok "Config: ~/.config/miflasher/"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗"
echo -e "║     MiFlasher installed successfully!   ║"
echo -e "╚══════════════════════════════════════════╝${RESET}"
echo ""
echo -e "${CYAN}Quick start:${RESET}"
echo -e "  ${DIM}source ~/.bashrc${RESET}        # Reload PATH"
echo -e "  ${CYAN}miflasher device${RESET}        # Detect connected device"
echo -e "  ${CYAN}miflasher unlock${RESET}        # Unlock bootloader"
echo -e "  ${CYAN}miflasher flash rom --path rom.zip${RESET}"
echo -e "  ${CYAN}miflasher gui${RESET}           # Web dashboard"
echo -e "  ${CYAN}miflasher --help${RESET}        # Full help"
echo ""
