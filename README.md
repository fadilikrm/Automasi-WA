<div align="center">

<h1 align="center">🤖 Bot Pengirim Pesan WhatsApp 🤖</h1>
<p align="center">
Sebuah bot sederhana untuk mengirim pesan WhatsApp secara otomatis berdasarkan data dari file Excel.
<br />
<a href="https://github.com/USERNAME/REPO/issues">Laporkan Bug</a>
·
<a href="https://github.com/USERNAME/REPO/issues">Minta Fitur Baru</a>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
<img src="https://img.shields.io/badge/Selenium-4-green?style=for-the-badge&logo=selenium" alt="Selenium">
<img src="https://img.shields.io/badge/Pandas-2-purple?style=for-the-badge&logo=pandas" alt="Pandas">
<br>
<img src="https://img.shields.io/github/license/USERNAME/REPO?style=for-the-badge" alt="License">
<img src="https://img.shields.io/github/last-commit/USERNAME/REPO?style=for-the-badge" alt="Last Commit">
<img src="https://img.shields.io/github/stars/USERNAME/REPO?style=social" alt="Stars">
</p>

PENTING: Jangan lupa mengganti USERNAME/REPO pada URL di atas dengan username dan nama repository GitHub Anda agar badge dapat berfungsi.

</div>

🧐 Tentang Proyek
Proyek ini adalah sebuah skrip otomasi yang berfungsi untuk:

Membaca daftar kontak (nama, nomor) dan isi pesan dari sebuah file Excel (data_pesan.xlsx).

Menggunakan Selenium untuk membuka WhatsApp Web di Google Chrome.

Menyimpan sesi login ke dalam folder chrome_profile_whatsapp agar Anda tidak perlu scan QR code berulang kali.

Mengirimkan pesan ke setiap kontak satu per satu sesuai data di Excel.

<br>
<div align="center">
<em>Tampilan struktur file dalam proyek:</em><br><br>
<img src="https://i.imgur.com/lO3i1QP.png" alt="[Struktur File Proyek]" width="400">
</div>
<br>

Dibangun Dengan
Berikut adalah beberapa library utama yang digunakan dalam proyek ini:

[][Selenium-url]

[][Pandas-url]

[][Openpyxl-url]

[][Webdriver-Manager-url]

🏁 Memulai
Untuk menjalankan salinan lokal, ikuti langkah-langkah sederhana berikut.

Prasyarat
Sebelum memulai, pastikan Anda sudah memiliki:

Python 3.9 atau yang lebih baru

Browser Google Chrome yang ter-install di komputer Anda

Instalasi
Clone repository ini (Ganti USERNAME/REPO dengan milik Anda)

git clone https://github.com/USERNAME/REPO.git

Masuk ke direktori proyek

cd NAMA-FOLDER-PROYEK

Buat dan aktifkan Virtual Environment (Sangat disarankan)

# Membuat venv
python -m venv .venv

# Aktivasi di Windows
.\.venv\Scripts\activate

# Aktivasi di MacOS/Linux
source .venv/bin/activate

Install semua library yang dibutuhkan dari requirements.txt

pip install -r requirements.txt

Isi data kontak Anda <br>
Buka file data_pesan.xlsx dan isi kolom nama, nomor (dengan format internasional, contoh: 6281234567890), dan pesan.

Login Pertama Kali (Scan QR) <br>
Jalankan skrip untuk pertama kali agar sesi login tersimpan.

python sendMessage.py

Sebuah jendela Chrome akan terbuka. Scan kode QR yang muncul menggunakan aplikasi WhatsApp di HP Anda. Setelah berhasil login, sesi akan otomatis tersimpan. Anda bisa menutup program jika sudah.

🎈 Penggunaan
Setelah instalasi dan login pertama berhasil, Anda bisa menjalankan bot dengan cara:

Pengguna Windows (Cara Mudah): Cukup klik dua kali file run.bat.

Semua Sistem Operasi: Jalankan perintah berikut di terminal Anda (pastikan virtual environment sudah aktif).

python sendMessage.py

Bot akan mulai mengirim pesan sesuai daftar di file Excel, dan progresnya akan ditampilkan di terminal.

⚠️ Peringatan (Disclaimer)
Gunakan tool ini dengan bijak. Pengiriman pesan massal dalam jumlah besar dan dalam waktu cepat dapat dianggap sebagai aktivitas spam oleh pihak WhatsApp dan berisiko tinggi membuat nomor Anda diblokir secara permanen. Pengembang tidak bertanggung jawab atas segala konsekuensi yang timbul dari penggunaan skrip ini.

📄 Lisensi
Didistribusikan di bawah Lisensi MIT. Lihat LICENSE.txt (jika ada) untuk informasi lebih lanjut.

☎️ Kontak
[NAMA ANDA] - [@akun_twitter_anda] - email@anda.com

Link Proyek: https://github.com/USERNAME/REPO

<!-- MARKDOWN LINKS & IMAGES -->

[]: #
[selenium-url]: https://www.google.com/search?q=%5Bhttps://www.selenium.dev/%5D(https://www.selenium.dev/)
[]: #
[pandas-url]: https://www.google.com/search?q=%5Bhttps://pandas.pydata.org/%5D(https://pandas.pydata.org/)
[]: #
[openpyxl-url]: https://www.google.com/search?q=%5Bhttps://openpyxl.readthedocs.io/en/stable/%5D(https://openpyxl.readthedocs.io/en/stable/)
[]: #
[webdriver-manager-url]: https://www.google.com/search?q=%5Bhttps://github.com/SergeyPirogov/webdriver_manager%5D(https://github.com/SergeyPirogov/webdriver_manager)
