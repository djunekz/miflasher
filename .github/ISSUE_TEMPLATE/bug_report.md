---
name: 🐛 Bug Report
about: Laporkan sesuatu yang tidak berjalan sebagaimana mestinya
title: "[BUG] "
labels: ["bug", "needs-triage"]
assignees: ""
---

<!--
  Sebelum membuka issue, pastikan kamu sudah:
  ✅ Membaca TROUBLESHOOTING.md
  ✅ Mencari issue yang sudah ada dengan masalah serupa
  ✅ Menjalankan ./miflasher --verbose untuk output lengkap

  Isi semua bagian di bawah dengan detail. Issue yang tidak lengkap
  akan membutuhkan waktu lebih lama untuk diperbaiki.
-->

## 🐛 Deskripsi Bug

<!-- Jelaskan bug secara singkat dan jelas -->



## 📋 Langkah Reproduksi

<!-- Jelaskan langkah-langkah untuk mereproduksi masalah ini -->

1. Jalankan perintah: `miflasher ...`
2. ...
3. Lihat error

## ✅ Perilaku yang Diharapkan

<!-- Apa yang seharusnya terjadi? -->



## ❌ Perilaku Aktual

<!-- Apa yang sebenarnya terjadi? -->



## 📄 Output Terminal (Wajib)

<!-- 
  Jalankan perintah dengan flag --verbose dan paste output lengkapnya.
  Jangan edit atau potong outputnya.
-->

```
$ ./miflasher [perintah] --verbose

paste output di sini
```

## 🖥️ Informasi Lingkungan

<!-- Isi tabel ini dengan lengkap -->

| Field | Value |
|---|---|
| MiFlasher version | <!-- `./miflasher --version` → contoh: v2.0.0 --> |
| Device model | <!-- contoh: Redmi Note 12 Pro --> |
| Device codename | <!-- Settings > About Phone > All Specs → contoh: ruby --> |
| Chipset | <!-- contoh: Snapdragon 778G --> |
| Android version | <!-- contoh: 13 --> |
| MIUI / HyperOS version | <!-- contoh: MIUI 14.0.6 --> |
| Termux version | <!-- `termux-info \| grep -i version` --> |
| Python version | <!-- `python3 --version` --> |
| ADB version | <!-- `adb version` --> |

## 🔌 Koneksi Device

<!-- Centang yang sesuai dengan kondisimu -->

- [ ] USB kabel biasa
- [ ] USB OTG adapter
- [ ] ADB over WiFi
- [ ] Device dalam mode ADB
- [ ] Device dalam mode Fastboot
- [ ] Device dalam mode Recovery
- [ ] Tidak ada device (error saat tidak connect)

## 📎 Informasi Tambahan

<!-- 
  Hal lain yang mungkin relevan:
  - Apakah ini baru terjadi? Versi sebelumnya berhasil?
  - Apakah ada langkah khusus yang kamu lakukan sebelumnya?
  - Screenshot jika diperlukan
-->



## ✔️ Checklist Sebelum Submit

- [ ] Sudah mencari issue yang sama dan tidak menemukannya
- [ ] Sudah membaca [TROUBLESHOOTING.md](https://github.com/djunekz/miflasher/blob/master/TROUBLESHOOTING.md)
- [ ] Sudah menjalankan dengan `--verbose` dan menyertakan output lengkap
- [ ] Sudah mengisi semua bagian di atas
