# WhatsApp Auto Sender 📱

Aplikasi otomatis untuk mengirim pesan WhatsApp secara massal menggunakan WhatsApp Web dengan dukungan pengiriman gambar dan teks.

## ✨ Fitur Utama

- 🔄 **Pengiriman Massal**: Kirim pesan ke banyak nomor sekaligus
- 📸 **Dukungan Gambar**: Kirim gambar dengan caption
- 💾 **Profile Persisten**: Tidak perlu scan QR code berulang kali
- 📊 **Excel Integration**: Baca data dari file Excel
- 🛡️ **Multiple Fallback**: Berbagai metode upload gambar untuk kompatibilitas maksimal
- 🔧 **Mode Manual**: Opsi manual jika otomatis gagal
- ⚡ **Robust Error Handling**: Penanganan error yang komprehensif

## 🚀 Cara Instalasi

### Prasyarat
- Python 3.7 atau lebih baru
- Google Chrome Browser (versi terbaru)
- Koneksi internet yang stabil

### Langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/whatsapp-auto-sender.git
   cd whatsapp-auto-sender
   ```

2. **Buat Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Aktivasi Virtual Environment**
   
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Persiapan Data

Buat file Excel dengan nama `data_pesan.xlsx` dengan struktur berikut:

| Nomor WhatsApp | Pesan | Gambar (opsional) |
|----------------|-------|-------------------|
| 628123456789 | Halo, ini pesan otomatis | gambar1.jpg |
| 628987654321 | Selamat pagi! | |
| 628111222333 | Promo spesial hari ini! | promo.png |

### Format Data:
- **Nomor WhatsApp**: Nomor dengan kode negara (contoh: 628123456789 untuk Indonesia)
- **Pesan**: Teks pesan yang akan dikirim
- **Gambar**: Path/nama file gambar (opsional, kosongkan jika hanya kirim teks)

### Format Gambar yang Didukung:
- JPG/JPEG
- PNG
- GIF
- BMP
- WEBP

## 🎯 Cara Penggunaan

### Metode 1: Jalankan dengan Batch File (Windows)
```bash
double-click run.bat
```

### Metode 2: Jalankan dengan Python
```bash
python sendMessage.py
```

### Metode 3: Jalankan dengan Virtual Environment
```bash
.venv\Scripts\python.exe sendMessage.py
```

## 📖 Panduan Penggunaan Lengkap

### 1. Setup Awal
- Jalankan aplikasi untuk pertama kali
- Browser Chrome akan terbuka secara otomatis
- Scan QR code WhatsApp Web dengan HP Anda
- **Penting**: Centang "Keep me signed in" jika tersedia
- Profile akan disimpan untuk penggunaan selanjutnya

### 2. Pengiriman Pesan
- Aplikasi akan membaca file `data_pesan.xlsx`
- Proses pengiriman dimulai secara otomatis
- Jeda 10 detik antar pesan untuk menghindari spam detection
- Log detail akan ditampilkan di console

### 3. Mode Manual (Fallback)
Jika upload gambar otomatis gagal, aplikasi akan memberikan instruksi manual:
- Klik tombol attachment di browser
- Pilih file gambar yang diminta
- Tambahkan caption jika diperlukan  
- Klik send

## 🔧 Konfigurasi Advanced

### Mengubah Jeda Waktu
Edit file `sendMessage.py` pada baris:
```python
time.sleep(10)  # Ubah angka 10 sesuai kebutuhan (dalam detik)
```

### Mengubah Lokasi Profile Chrome
Edit variabel `chrome_profile_dir` di fungsi `create_driver()`:
```python
chrome_profile_dir = os.path.join(script_dir, "chrome_profile_whatsapp")
```

## 🛠️ Troubleshooting

### Masalah Umum dan Solusi

#### 1. WebDriver Error
```
Gagal membuat WebDriver!
```
**Solusi:**
- Jalankan Command Prompt sebagai Administrator
- Update Google Chrome ke versi terbaru
- Restart komputer
- Hapus folder `chrome_profile_whatsapp` jika ada

#### 2. QR Code Tidak Muncul
**Solusi:**
- Refresh halaman browser
- Hapus folder `chrome_profile_whatsapp`
- Jalankan ulang aplikasi

#### 3. Gambar Tidak Terupload
**Solusi:**
- Pastikan file gambar ada di folder yang benar
- Cek format file gambar (harus JPG, PNG, GIF, BMP, atau WEBP)
- Gunakan mode manual jika otomatis gagal

#### 4. Nomor Tidak Valid
```
Nomor 628123456789 tidak valid
```
**Solusi:**
- Pastikan nomor dimulai dengan kode negara
- Hapus spasi, tanda hubung, atau karakter khusus
- Pastikan nomor terdaftar di WhatsApp

### Error Logs
Aplikasi akan menampilkan log detail di console. Perhatikan pesan:
- ✅ Sukses
- ⚠️ Warning
- ❌ Error

## 📁 Struktur Folder

```
whatsapp-auto-sender/
├── sendMessage.py          # Script utama
├── run.bat                 # Batch file untuk Windows
├── requirements.txt        # Dependencies
├── data_pesan.xlsx        # File data (buat sendiri)
├── chrome_profile_whatsapp/ # Profile Chrome (otomatis)
├── gambar1.jpg            # Contoh gambar
├── gambar2.png            # Contoh gambar
└── README.md              # Dokumentasi ini
```

## 🔒 Keamanan dan Privasi

### Penting untuk Diperhatikan:
- **Jangan share profile Chrome** dengan orang lain
- **Gunakan nomor yang valid** dan sudah memberikan consent
- **Patuhi kebijakan WhatsApp** tentang penggunaan otomatis
- **Jangan spam** - gunakan jeda waktu yang wajar
- **Backup data** secara berkala

### Rekomendasi Keamanan:
- Gunakan di komputer pribadi
- Logout WhatsApp Web setelah selesai
- Jangan tinggalkan aplikasi berjalan tanpa pengawasan

## 🤝 Contributing

Kami menerima kontribusi! Silakan:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/fitur-baru`)
3. Commit perubahan (`git commit -am 'Tambah fitur baru'`)
4. Push ke branch (`git push origin feature/fitur-baru`)
5. Buat Pull Request

### Pedoman Kontribusi:
- Ikuti coding style yang ada
- Tambahkan dokumentasi untuk fitur baru
- Test semua perubahan sebelum submit
- Gunakan commit message yang jelas

## 📝 Changelog

### v2.0.0 (Latest)
- ✅ Dukungan upload gambar dengan multiple fallback methods
- ✅ Profile Chrome persisten
- ✅ Improved error handling
- ✅ Mode manual untuk fallback
- ✅ Detailed logging

### v1.0.0
- ✅ Pengiriman pesan teks massal
- ✅ Integrasi Excel
- ✅ Basic error handling

## 📞 Support

Jika mengalami masalah:

1. **Cek FAQ** di atas terlebih dahulu
2. **Buka Issue** di GitHub dengan detail:
   - Versi Python
   - Versi Chrome
   - Error message lengkap
   - Langkah yang sudah dicoba

## ⚖️ Disclaimer

- Aplikasi ini untuk tujuan edukasi dan otomasi legitimate
- Pengguna bertanggung jawab atas penggunaan aplikasi
- Patuhi Terms of Service WhatsApp
- Jangan gunakan untuk spam atau aktivitas ilegal

## 📄 License

MIT License - Silakan gunakan dengan bebas untuk keperluan personal maupun komersial.

## 🙏 Acknowledgments

- [Selenium](https://selenium.dev/) - Web automation framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation library
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) - Automatic driver management
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel file handling

---

### 📧 Kontak

Untuk pertanyaan atau saran, silakan buka issue di GitHub repository ini.

**Happy Automating! 🚀**
