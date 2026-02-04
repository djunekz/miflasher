#!/usr/bin/env bash
set -e
echo "[..] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[..] Installing Python3..."
pkg install python3 -y
pip install --upgrade pip

echo "[..] Installing dependencies..."
pkg install pv libusb -y
pip install -r requirements.txt

echo "[..] Making CLI executable..."
chmod +x miflasher
ln -sf $(pwd)/miflasher $PREFIX/bin/miflasher

echo "[✔] Installation completed!"
