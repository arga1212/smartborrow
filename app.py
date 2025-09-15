# app.py
import streamlit as st
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import Borrowing
from ai_client import ask_gemini
import json

# Pastikan tabel dibuat
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="SmartBorrow Prototype", layout="wide")

# ---------- Utils ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def csv_to_list(s: str):
    if not s:
        return []
    # robust split: strip whitespace
    return [item.strip() for item in s.split(",") if item.strip()]

def list_to_csv(lst):
    return ",".join(lst)

# ---------- Sidebar / Login ----------
st.sidebar.title("SmartBorrow Prototype")
role = st.sidebar.selectbox("Login sebagai", options=["User", "Admin"])
username = st.sidebar.text_input("Nama", value="Siswa1")

# ---------- Main ----------
if role == "User":
    st.title("📦 SmartBorrow — Peminjaman Barang & Ruangan")
    st.markdown("Gunakan AI untuk dapat rekomendasi barang, lalu ajukan peminjaman.")

    st.subheader("💬 Tanya AI Asisten")
    activity = st.text_input("Kegiatan kamu apa?", value="Saya mau bikin podcast")
    if st.button("Dapatkan Rekomendasi"):
        with st.spinner("Menghubungi AI..."):
            prompt = f"Saya mau {activity}. Barang dan ruangan apa saja yang dibutuhkan? Berikan dalam format daftar terpisah koma."
            try:
                rec_text = ask_gemini(prompt)
            except Exception as e:
                st.error(f"Gagal ke AI: {e}")
                rec_text = "Ruang podcast, 2 mic, 2 headset, laptop, kabel, meja"
            st.session_state["recommendation"] = rec_text

    if "recommendation" in st.session_state:
        st.write("AI merekomendasikan (bisa diedit):")
        items_text = st.text_area("Daftar Barang (pisahkan dengan koma)", value=st.session_state["recommendation"])
        if st.button("Ajukan Peminjaman"):
            # insert to DB
            db = next(get_db())
            b = Borrowing(user=username, items=items_text, status="Menunggu", taken="", returned="")
            db.add(b)
            db.commit()
            st.success("Peminjaman diajukan. Menunggu persetujuan admin.")
            st.rerun()


    st.subheader("📊 Riwayat & Checklist")
    db = next(get_db())
    rows = db.query(Borrowing).filter(Borrowing.user == username).order_by(Borrowing.created_at.desc()).all()
    if not rows:
        st.info("Belum ada riwayat peminjaman.")
    for row in rows:
        st.markdown("---")
        st.write(f"**ID**: {row.id}  |  **Status**: {row.status}  |  **Diajukan**: {row.created_at}")
        st.write(f"**Barang**: {row.items}")

        # jika disetujui -> tampilkan checklist ambil
        if row.status == "Disetujui":
            st.info("Silakan ambil barang sesuai checklist lalu klik 'Mulai Kegiatan'")
            items_list = csv_to_list(row.items)
            chosen = st.multiselect("Checklist Barang Diambil", items_list, key=f"ambil_{row.id}")
            if st.button(f"Mulai Kegiatan (ID {row.id})"):
                row.taken = list_to_csv(chosen)
                row.status = "Checklist Ambil"
                db.add(row)
                db.commit()
                st.success("Barang dicatat sebagai diambil. Semoga kegiatan lancar!")
                st.rerun()


        # jika sudah mulai -> tampilkan checklist pengembalian
        if row.status == "Checklist Ambil":
            st.info("Sudah mulai. Setelah selesai, lengkapi checklist pengembalian.")
            items_list = csv_to_list(row.items)
            returned = st.multiselect("Checklist Barang Dikembalikan", items_list, key=f"kembali_{row.id}")
            if st.button(f"Selesaikan Peminjaman (ID {row.id})"):
                row.returned = list_to_csv(returned)
                row.status = "Selesai"
                db.add(row)
                db.commit()
                st.success("Peminjaman selesai. Terima kasih sudah mengembalikan.")
                st.rerun()


        # tampilkan taken/returned jika ada
        if row.taken:
            st.write(f"✅ Barang diambil: {row.taken}")
        if row.returned:
            st.write(f"🔁 Barang dikembalikan: {row.returned}")

if role == "Admin":
    st.title("🛠️ Dashboard Admin")
    st.markdown("Kelola pengajuan peminjaman di bawah ini.")

    db = next(get_db())
    rows = db.query(Borrowing).order_by(Borrowing.created_at.desc()).all()
    if not rows:
        st.info("Belum ada pengajuan.")
    for row in rows:
        st.markdown("---")
        st.write(f"**ID**: {row.id}  |  **User**: {row.user}  |  **Status**: {row.status}  |  **Diajukan**: {row.created_at}")
        st.write(f"**Barang**: {row.items}")
        if row.taken:
            st.write(f"✅ Diambil: {row.taken}")
        if row.returned:
            st.write(f"🔁 Dikembalikan: {row.returned}")

        if row.status == "Menunggu":
            cols = st.columns(3)
            if cols[0].button(f"✅ Approve {row.id}"):
                row.status = "Disetujui"
                db.add(row); db.commit(); st.rerun()

            if cols[1].button(f"❌ Reject {row.id}"):
                row.status = "Ditolak"
                db.add(row); db.commit(); st.rerun()

            if cols[2].button(f"🗑️ Hapus {row.id}"):
                db.delete(row); db.commit(); st.rerun()

