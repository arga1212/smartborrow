# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class Borrowing(Base):
    __tablename__ = "borrowings"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), nullable=False)
    items = Column(Text, default="")         # CSV / JSON string of items
    status = Column(String(50), default="Menunggu")  # Menunggu, Disetujui, Ditolak, Checklist Ambil, Selesai
    taken = Column(Text, default="")         # CSV items taken
    returned = Column(Text, default="")      # CSV items returned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
