---
name: 📊 Compatibility Report
about: Laporkan hasil testing MiFlasher di device kamu (berhasil maupun tidak)
title: "[COMPAT] "
labels: ["compatibility"]
assignees: ""
---

<!--
  Laporan kompatibilitas sangat membantu kami dan pengguna lain!
  Kamu tidak perlu device yang bermasalah untuk membuat laporan ini —
  laporan "device X berjalan sempurna" juga sangat berharga.

  Isi semua bagian yang kamu bisa. Bagian yang tidak relevan boleh dikosongi.
-->

## 📱 Informasi Device

| Field | Value |
|---|---|
| Device name | <!-- contoh: Redmi Note 12 Pro --> |
| Codename | <!-- Settings > About Phone > All Specs → contoh: ruby --> |
| Chipset / SoC | <!-- contoh: Snapdragon 778G 5G --> |
| RAM | <!-- contoh: 8 GB --> |
| Android version | <!-- contoh: 13 (API 33) --> |
| MIUI / HyperOS version | <!-- contoh: MIUI 14.0.6 Global --> |
| Region variant | <!-- contoh: Global / China / India / EEA --> |
| Slot type | <!-- A-only / A/B (VAB) / tidak tahu --> |
| Bootloader status | <!-- Locked / Unlocked / tidak tahu --> |

## 🧪 Hasil Testing

<!--
  Centang dan isi kolom "Catatan" untuk setiap fitur yang kamu test.
  Gunakan: ✅ Berhasil | ⚠️ Sebagian | ❌ Gagal | ➖ Tidak ditest
-->

| Perintah | Status | Catatan |
|---|---|---|
| `miflasher device` | | |
| `miflasher device --watch` | | |
| `miflasher device --reboot bootloader` | | |
| `miflasher unlock` | | |
| `miflasher unlock --fastboot-only` | | |
| `miflasher flash boot` | | |
| `miflasher flash rom` | | |
| `miflasher flash recovery` | | |
| `miflasher flash vbmeta` | | |
| `miflasher flash payload` | | |
| `miflasher backup --all` | | |
| `miflasher restore` | | |
| `miflasher wipe` | | |
| `miflasher gui` | | |

## 📄 Output untuk Fitur yang Gagal

<!--
  Untuk setiap fitur yang ❌ atau ⚠️, paste output terminal di sini.
  Jalankan dengan --verbose untuk output yang lebih detail.
-->

<details>
<summary>Output error (klik untuk expand)</summary>

```
$ ./miflasher [perintah] --verbose

paste output di sini
```

</details>

## ⚠️ Masalah atau Keanehan yang Ditemukan

<!-- 
  Apakah ada perilaku tidak terduga meskipun tidak error?
  Contoh: "Backup berhasil tapi ukuran file sangat kecil"
-->



## 💡 Workaround (jika ada)

<!-- 
  Jika kamu menemukan cara untuk mengatasi masalah di atas, 
  bagikan di sini agar bisa membantu pengguna lain dengan device serupa.
-->



## 🖥️ Informasi Lingkungan

| Field | Value |
|---|---|
| MiFlasher version | <!-- `./miflasher --version` --> |
| Termux version | <!-- `termux-info \| grep -i version` --> |
| Python version | <!-- `python3 --version` --> |
| ADB version | <!-- `adb version` --> |
| Koneksi | <!-- USB kabel / USB OTG / ADB WiFi --> |

## 📎 Informasi Tambahan

<!-- Screenshot, foto layar device, atau konteks lain yang relevan -->
