# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    # ... (Isi class User tidak berubah, biarkan saja)
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='siswa')
    peminjaman = db.relationship('Peminjaman', backref='peminjam', lazy=True)

class Barang(db.Model):
    # ... (Isi class Barang tidak berubah, biarkan saja)
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(150), nullable=False)
    jumlah_total = db.Column(db.Integer, nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)

# --- TAMBAHAN BARU ---
class Ruangan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_ruangan = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)

class Peminjaman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_acara = db.Column(db.String(200), nullable=False)
    tanggal_pinjam = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Menunggu Persetujuan')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # --- MODIFIKASI: Tambahkan foreign key untuk ruangan ---
    ruangan_id = db.Column(db.Integer, db.ForeignKey('ruangan.id'), nullable=True) # nullable=True artinya boleh kosong
    
    # Relasi
    ruangan = db.relationship('Ruangan')
    detail = db.relationship('DetailPeminjaman', backref='peminjaman', lazy=True, cascade="all, delete-orphan")

class DetailPeminjaman(db.Model):
    # ... (Isi class DetailPeminjaman tidak berubah, biarkan saja)
    id = db.Column(db.Integer, primary_key=True)
    peminjaman_id = db.Column(db.Integer, db.ForeignKey('peminjaman.id'), nullable=False)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    jumlah_pinjam = db.Column(db.Integer, nullable=False)
    status_barang = db.Column(db.String(50), default='Dipinjam')
    barang = db.relationship('Barang')