# 📲 WhatsApp Auto Sender with Text and Image (Python)

Skript Python ini digunakan untuk mengirim pesan WhatsApp secara otomatis ke kontak tertentu, dengan data yang diambil dari file Excel. Fitur ini mendukung pengiriman teks dan gambar (opsional), dan memanfaatkan beberapa library seperti `pywhatkit`, `pyautogui`, dan `pynput`.

## 🛠️ Fitur
- ✅ Kirim pesan teks otomatis melalui WhatsApp Web
- 🖼️ Opsi untuk mengirim gambar bersama pesan
- 📊 Data penerima dan pesan diambil dari file Excel
- ⏱️ Delay otomatis agar aman digunakan (anti blokir)

## 🧾 Struktur File Excel
Pastikan file Excel kamu (misalnya `data_pesan.xlsx`) memiliki format seperti berikut:

| Nomor WhatsApp | Pesan                  | Gambar              |
|----------------|------------------------|---------------------|
| 6281234567890  | Halo, ini pesan tes    | path/to/image.jpg   |
| 6289876543210  | Selamat pagi!          | (kosong jika tanpa gambar) |

**Catatan:**
- Nomor WhatsApp harus dimulai dengan kode negara (contoh: `62` untuk Indonesia).
- Kolom `Gambar` bisa dikosongkan jika hanya ingin mengirim teks.

## 📦 Library yang Digunakan
Pastikan kamu sudah menginstal library berikut:

```bash
pip install pywhatkit pyautogui pandas pynput
