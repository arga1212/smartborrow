🧠 Asistio — Sistem Manajemen Peminjaman Sekolah Berbasis AI

Asistio adalah aplikasi web berbasis Flask + AI (Google Gemini) yang dirancang untuk mempermudah proses peminjaman barang dan ruangan sekolah.
Dengan bantuan AI, siswa cukup menulis deskripsi acara mereka, dan sistem otomatis merekomendasikan ruangan serta perlengkapan yang dibutuhkan.
Guru (admin) dapat mengelola inventaris dan menyetujui peminjaman dengan efisien.

🚀 Fitur Utama
👩‍🏫 Sistem Login Berbasis Peran

Siswa → dapat mengajukan peminjaman.

Guru/Admin → mengelola data barang, ruangan, dan menyetujui peminjaman.

🤖 Peminjaman Cerdas (AI)

Siswa cukup menulis deskripsi acara (contoh: “Saya mau adakan podcast di aula, butuh mic dan lighting.”).

AI (Google Gemini) akan memberikan rekomendasi ruangan dan barang otomatis dari inventaris sekolah.

📝 Peminjaman Manual

Pengguna yang sudah tahu kebutuhan acara bisa memilih barang dan ruangan secara langsung.

🧰 Manajemen Inventaris & Ruangan

CRUD Barang (Tambah, Lihat, Edit, Hapus)

CRUD Ruangan (Tambah, Lihat, Edit, Hapus)

📊 Dashboard & Riwayat

Siswa: Melihat status dan riwayat peminjaman pribadi.

Guru: Melihat seluruh pengajuan peminjaman sekolah.

✅ Alur Persetujuan

Guru dapat menyetujui atau menolak peminjaman yang diajukan siswa.

🧩 Teknologi yang Digunakan
Komponen	Teknologi
Backend	Flask (Python 3)
Database	SQLite + SQLAlchemy ORM
Frontend	HTML, CSS, JavaScript, Bootstrap 5
AI Engine	Google Gemini (gemini-1.0-pro)
Keamanan	Flask-Login (autentikasi), Flask-Bcrypt (enkripsi password)
⚙️ Instalasi & Setup

Langkah-langkah untuk menjalankan Asistio di komputer kamu:

1. Prasyarat

Pastikan sudah terinstal:

Python 3.8+

pip

venv (biasanya sudah ada dalam instalasi Python)

2. Clone Proyek
git clone https://github.com/username-kamu/asistio.git
cd asistio

3. Buat dan Aktifkan Virtual Environment
🧠 macOS / Linux
python3 -m venv venv
source venv/bin/activate

🪟 Windows
python -m venv venv
venv\Scripts\activate

4. Install Semua Dependensi

Gunakan file requirements.txt yang sudah disediakan:

pip install -r requirements.txt

5. Tambahkan API Key Gemini

Buat file .env di folder proyek.

Tambahkan isi berikut:

GEMINI_API_KEY="MASUKKAN_API_KEY_KAMU_DI_SINI"


⚠️ Jangan pernah upload file .env ke GitHub atau membagikannya ke orang lain.

6. Jalankan Aplikasi
python app.py


Buka browser dan akses:
👉 http://127.0.0.1:5000

🧭 Panduan Penggunaan Pertama Kali

Reset Database (opsional)
Hapus file asistio.db jika ingin memulai dari nol, lalu jalankan ulang server.

Buat Akun Guru (Admin)
Akun pertama yang didaftarkan otomatis menjadi Guru/Admin.

Login sebagai Guru
Tambahkan data ruangan dan barang di menu Manajemen.

Buat Akun Siswa
Logout, lalu buat akun baru — akun ini dan berikutnya otomatis berperan sebagai Siswa.

Gunakan Fitur Peminjaman Cerdas
Login sebagai siswa → buka Buat Peminjaman → isi deskripsi acara → klik “Dapatkan Rekomendasi AI”.

Guru Menyetujui Peminjaman
Login sebagai guru → buka dashboard → setujui/tolak peminjaman yang diajukan siswa.

📁 Struktur Proyek
smartborrow/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── (script tambahan)
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── inventaris.html
│   ├── login.html
│   ├── pinjam.html
│   ├── pinjam_manual.html
│   ├── register.html
│   ├── riwayat.html
│   └── ruangan.html
│
├── app.py
├── models.py
├── asistio.db
├── requirements.txt
└── README.md

💡 Tips Tambahan

Gunakan flask run agar server berjalan dengan debug mode.

Simpan aset CSS/JS di folder static/.

Siapkan Procfile dan requirements.txt jika ingin deploy ke Render, Railway, atau Vercel.

📬 Kontribusi

Fork repository ini.

Buat branch baru: feature/nama-fitur.

Commit dan push perubahanmu.

Buat Pull Request ke repositori utama.

🧑‍💻 Lisensi

Proyek ini dibuat 🌟🌟🌟🌟🌟 oleh o,eh.
Bebas digunakan untuk pembelajaran, penelitian, dan pengembangan.