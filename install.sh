#!/usr/bin/env bash
set -e
echo "[..] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[..] Installing Python3 and dependencies..."
pkg install python3 pv libusb -y
pip install --upgrade pip
pip install -r requirements.txt

chmod +x miflasher
ln -sf $(pwd)/miflasher $PREFIX/bin/miflasher

echo "[✔] Installation completed!"
