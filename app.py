# app.py
import os
import google.generativeai as genai
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from datetime import datetime
# PENAMBAHAN 1: Import Ruangan yang hilang dari models.py
from models import db, User, Barang, Peminjaman, DetailPeminjaman, Ruangan
from functools import wraps

# --- KONFIGURASI APLIKASI ---
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-yang-sangat-aman'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asistio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "warning"

# Konfigurasi Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # PENYEMPURNAAN: Menggunakan model yang stabil dan lebih baru
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Anda tidak memiliki izin untuk mengakses halaman ini.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- RUTE-RUTE HALAMAN (VIEWS) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # ... (Fungsi ini sudah benar, tidak perlu diubah)
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nama = request.form.get('nama')
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar.', 'danger')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        role = 'guru' if User.query.count() == 0 else 'siswa'
        new_user = User(nama=nama, username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Akun berhasil dibuat sebagai {role}! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... (Fungsi ini sudah benar, tidak perlu diubah)
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login gagal. Periksa kembali username dan password Anda.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'guru':
        peminjaman_list = Peminjaman.query.order_by(Peminjaman.tanggal_pinjam.desc()).all()
    else:
        peminjaman_list = Peminjaman.query.filter_by(user_id=current_user.id).order_by(Peminjaman.tanggal_pinjam.desc()).all()
    return render_template('dashboard.html', peminjaman_list=peminjaman_list)

# PENAMBAHAN 2: Rute untuk halaman pinjam manual yang hilang
@app.route('/pinjam/manual')
@login_required
def pinjam_manual():
    list_ruangan = Ruangan.query.order_by(Ruangan.nama_ruangan).all()
    list_barang = Barang.query.order_by(Barang.nama_barang).all()
    return render_template('pinjam_manual.html', list_ruangan=list_ruangan, list_barang=list_barang)

@app.route('/pinjam', methods=['GET'])
@login_required
def pinjam():
    # MODIFIKASI: Kirim daftar ruangan ke template
    semua_ruangan = Ruangan.query.all()
    return render_template('pinjam.html', semua_ruangan=semua_ruangan)

@app.route('/ajukan-peminjaman', methods=['POST'])
@login_required
def ajukan_peminjaman():
    # ... (Fungsi ini sudah benar, tidak perlu diubah)
    data = request.get_json()
    try:
        ruangan_id = data.get('ruangan_id')
        if ruangan_id == "": ruangan_id = None
        peminjaman_baru = Peminjaman(
            nama_acara=data['nama_acara'],
            tanggal_pinjam=datetime.strptime(data['tanggal_pinjam'], '%Y-%m-%d').date(),
            user_id=current_user.id,
            ruangan_id=ruangan_id
        )
        db.session.add(peminjaman_baru)
        db.session.commit()
        for item in data.get('items', []):
            barang = None
            if 'nama' in item:
                barang = Barang.query.filter_by(nama_barang=item['nama']).first()
            elif 'id' in item:
                barang = db.session.get(Barang, item['id'])
            if barang:
                detail = DetailPeminjaman(peminjaman_id=peminjaman_baru.id, barang_id=barang.id, jumlah_pinjam=item['jumlah'])
                db.session.add(detail)
        db.session.commit()
        flash('Pengajuan peminjaman berhasil dikirim!', 'success')
        return jsonify({'success': True, 'redirect_url': url_for('dashboard')})
    except Exception as e:
        db.session.rollback()
        print(f"Error saat mengajukan peminjaman: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/inventaris', methods=['GET', 'POST'])
@login_required
@role_required('guru')
def inventaris():
    if request.method == 'POST':
        barang_baru = Barang(nama_barang=request.form.get('nama_barang'), jumlah_total=request.form.get('jumlah'), deskripsi=request.form.get('deskripsi'))
        db.session.add(barang_baru)
        db.session.commit()
        flash('Barang berhasil ditambahkan!', 'success')
        return redirect(url_for('inventaris'))
    return render_template('inventaris.html', list_barang=Barang.query.all())

@app.route('/inventaris/edit/<int:id>', methods=['POST'])
@login_required
@role_required('guru')
def edit_inventaris(id):
    # PENYEMPURNAAN: Menggunakan db.session.get()
    barang = db.session.get(Barang, id)
    barang.nama_barang = request.form.get('nama_barang')
    barang.jumlah_total = request.form.get('jumlah')
    barang.deskripsi = request.form.get('deskripsi')
    db.session.commit()
    flash('Data barang berhasil diperbarui.', 'success')
    return redirect(url_for('inventaris'))

@app.route('/inventaris/hapus/<int:id>', methods=['POST'])
@login_required
@role_required('guru')
def hapus_inventaris(id):
    # PENYEMPURNAAN: Menggunakan db.session.get()
    barang = db.session.get(Barang, id)
    db.session.delete(barang)
    db.session.commit()
    flash('Barang berhasil dihapus.', 'success')
    return redirect(url_for('inventaris'))

@app.route('/ruangan', methods=['GET', 'POST'])
@login_required
@role_required('guru')
def ruangan():
    if request.method == 'POST':
        ruangan_baru = Ruangan(nama_ruangan=request.form.get('nama_ruangan'), deskripsi=request.form.get('deskripsi'))
        db.session.add(ruangan_baru)
        db.session.commit()
        flash('Ruangan berhasil ditambahkan!', 'success')
        return redirect(url_for('ruangan'))
    return render_template('ruangan.html', list_ruangan=Ruangan.query.all())

@app.route('/ruangan/edit/<int:id>', methods=['POST'])
@login_required
@role_required('guru')
def edit_ruangan(id):
    ruangan = db.session.get(Ruangan, id)
    ruangan.nama_ruangan = request.form.get('nama_ruangan')
    ruangan.deskripsi = request.form.get('deskripsi')
    db.session.commit()
    flash('Data ruangan berhasil diperbarui.', 'success')
    return redirect(url_for('ruangan'))

@app.route('/ruangan/hapus/<int:id>', methods=['POST'])
@login_required
@role_required('guru')
def hapus_ruangan(id):
    ruangan = db.session.get(Ruangan, id)
    db.session.delete(ruangan)
    db.session.commit()
    flash('Ruangan berhasil dihapus.', 'success')
    return redirect(url_for('ruangan'))

@app.route('/peminjaman/setujui/<int:id>', methods=['POST'])
@login_required
@role_required('guru')
def setujui_peminjaman(id):
    # PENYEMPURNAAN: Menggunakan db.session.get()
    peminjaman = db.session.get(Peminjaman, id)
    peminjaman.status = 'Disetujui'
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/peminjaman/tolak/<int:id>', methods=['POST'])
@login_required
@role_required('guru')
def tolak_peminjaman(id):
    # PENYEMPURNAAN: Menggunakan db.session.get()
    peminjaman = db.session.get(Peminjaman, id)
    peminjaman.status = 'Ditolak'
    db.session.commit()
    return redirect(url_for('dashboard'))

# --- RUTE API UNTUK AI ---
@app.route('/api/rekomendasi-ai', methods=['POST'])
@login_required
def rekomendasi_ai():
    if not model: return jsonify({'error': 'Layanan AI tidak terkonfigurasi.'}), 500
    
    deskripsi_acara = request.get_json().get('deskripsi')
    if not deskripsi_acara: return jsonify({'error': 'Deskripsi acara kosong.'}), 400
    
    # PERUBAHAN 1: Ambil juga daftar RUANGAN dari database
    daftar_barang_str = ", ".join([b.nama_barang for b in Barang.query.all()]) or "Tidak ada"
    daftar_ruangan_str = ", ".join([r.nama_ruangan for r in Ruangan.query.all()]) or "Tidak ada"

    # PERUBAHAN 2: Buat prompt yang lebih canggih untuk merekomendasikan ruangan DAN barang
    prompt = f"""
    Anda adalah AI asisten untuk sistem peminjaman sekolah bernama Asistio.
    Siswa akan mengadakan acara: "{deskripsi_acara}".
    
    Daftar RUANGAN yang tersedia: [{daftar_ruangan_str}].
    Daftar BARANG yang tersedia: [{daftar_barang_str}].
    
    Berdasarkan deskripsi acara, berikan rekomendasi:
    1.  Satu ruangan yang paling sesuai (jika dibutuhkan).
    2.  Daftar barang yang mungkin dibutuhkan.

    Respons HANYA dalam format JSON tunggal yang valid. Strukturnya harus seperti ini:
    {{
      "ruangan": "Nama Ruangan yang Direkomendasikan",
      "barang": [
        {{"nama": "Nama Barang 1", "jumlah": 1}},
        {{"nama": "Nama Barang 2", "jumlah": 5}}
      ]
    }}

    Jika tidak ada ruangan yang cocok, nilai "ruangan" harus null.
    Jika tidak ada barang yang cocok, nilai "barang" harus array kosong [].
    """
    
    try:
        response = model.generate_content(prompt)
        clean_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(clean_response)
        return jsonify(parsed_json)
    except Exception as e:
        print(f"Terjadi error saat menghubungi API Gemini: {e}")
        return jsonify({'error': 'Gagal mendapat rekomendasi dari AI.'}), 500
# --- INISIALISASI DATABASE & JALANKAN APLIKASI ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)