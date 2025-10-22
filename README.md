📦 SmartBorrow Prototype

SmartBorrow adalah aplikasi prototipe berbasis **Streamlit + SQLAlchemy + Gemini AI** untuk mengelola peminjaman barang & ruangan dengan bantuan asisten AI.

🚀 Fitur
- 🔑 Login sebagai **User** atau **Admin**
- 💬 AI Asisten (Gemini) untuk rekomendasi barang/ruangan sesuai kegiatan
- 📦 User bisa mengajukan peminjaman, checklist ambil, checklist pengembalian
- 🛠️ Admin bisa approve, reject, atau hapus pengajuan
- 🗄️ Database menggunakan **SQLite + SQLAlchemy**

---

⚙️ Setup

1. clone repo & masuk ke folder project
   git clone https://github.com/arga1212/smartborrow.git
   cd smartborrow

2. Buat virtual environment

   bash
   python -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   .venv\Scripts\activate      # Windows


3. install dependencies

   bash
   pip install -r requirements.txt

4. Buat file .env untuk API key Gemini

   env
   GEMINI_API_KEY=your_api_key_here

5. Jalankan aplikasi

   bash
   python -m streamlit run app.py

 📂 Struktur Project

smartborrow/
│── app.py           # Main Streamlit app
│── db.py            # Database engine & session
│── models.py        # SQLAlchemy ORM models
│── ai_client.py     # Koneksi ke Gemini API
│── requirements.txt # Dependency list
│── .env             # Gemini API key (tidak di-push ke GitHub)


📜 Lisensi

Proyek ini hanya prototipe untuk kebutuhan pembelajaran. Silakan dikembangkan lebih lanjut sesuai kebutuhan.
