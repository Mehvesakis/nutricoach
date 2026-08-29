from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# --- 1. YENİ VERİTABANI MİMARİSİ (LEVEL 2) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./nuticoach.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# YENİ TABLO: Sol menüde duracak sohbet klasörleri
class SohbetOturumu(Base):
    __tablename__ = "oturumlar"
    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String)

# GÜNCELLENEN TABLO: Mesajlar artık hangi klasörde (oturum_id) olduğunu biliyor
class MesajKaydi(Base):
    __tablename__ = "mesajlar"
    id = Column(Integer, primary_key=True, index=True)
    oturum_id = Column(Integer) 
    rol = Column(String)
    icerik = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KullaniciMesaji(BaseModel):
    mesaj: str

# --- 2. GOOGLE API ---
# BURAYA KENDİ ANAHTARINI YAPIŞTIRMAYI UNUTMA!
import os
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

def kurallari_oku():
    try:
        with open("diyet_kurallari.txt", "r", encoding="utf-8") as dosya:
            return dosya.read()
    except FileNotFoundError:
        return "Sen yardımcı bir asistansın."

model = genai.GenerativeModel(
    model_name='models/gemini-3.6-flash',
    system_instruction=kurallari_oku()
)

# --- 3. YENİ API KAPILARI (Sol Menü İçin) ---

@app.post("/yeni_oturum")
async def yeni_oturum_ac():
    db = SessionLocal()
    su_an = datetime.now().strftime("%H:%M")
    yeni_oturum = SohbetOturumu(baslik=f"Yeni Sohbet ({su_an})")
    db.add(yeni_oturum)
    db.commit()
    db.refresh(yeni_oturum)
    oturum_id = yeni_oturum.id
    db.close()
    return {"id": oturum_id, "baslik": yeni_oturum.baslik}

@app.get("/oturumlar")
async def oturumlari_getir():
    db = SessionLocal()
    # Oturumları en yeniden en eskiye doğru sırala
    oturumlar_db = db.query(SohbetOturumu).order_by(SohbetOturumu.id.desc()).all()
    db.close()
    return {"oturumlar": [{"id": o.id, "baslik": o.baslik} for o in oturumlar_db]}

@app.get("/gecmis/{oturum_id}")
async def gecmisi_getir(oturum_id: int):
    db = SessionLocal()
    gecmis_mesajlar_db = db.query(MesajKaydi).filter(MesajKaydi.oturum_id == oturum_id).order_by(MesajKaydi.id).all()
    db.close()
    
    formatli_gecmis = []
    for m in gecmis_mesajlar_db:
        formatli_gecmis.append({"rol": m.rol, "icerik": m.icerik})
    return {"mesajlar": formatli_gecmis}

@app.post("/sohbet/{oturum_id}")
async def sohbet_et(oturum_id: int, istek: KullaniciMesaji):
    db = SessionLocal()
    
    # Yeni mesajı kaydet
    yeni_kullanici_mesaji = MesajKaydi(oturum_id=oturum_id, rol="user", icerik=istek.mesaj)
    db.add(yeni_kullanici_mesaji)
    db.commit()

    # Sadece bu oturuma ait geçmişi çek (Gemini hafızası için)
    gecmis_mesajlar_db = db.query(MesajKaydi).filter(MesajKaydi.oturum_id == oturum_id).order_by(MesajKaydi.id).all()
    
    gecmis = []
    for m in gecmis_mesajlar_db:
        gecmis.append({"role": m.rol, "parts": [m.icerik]})

    try:
        chat = model.start_chat(history=gecmis[:-1]) 
        response = chat.send_message(istek.mesaj)
        temiz_cevap = response.text
        
        # Harika Detay: İlk mesaj gönderildiğinde sohbetin başlığını otomatik değiştir!
        oturum = db.query(SohbetOturumu).filter(SohbetOturumu.id == oturum_id).first()
        if oturum and len(gecmis_mesajlar_db) <= 2:
            oturum.baslik = (istek.mesaj[:25] + '...') if len(istek.mesaj) > 25 else istek.mesaj
            db.commit()

    except Exception as e:
        temiz_cevap = f"Yapay zeka bağlantı hatası: {str(e)}"

    if "bağlantı hatası" not in temiz_cevap:
        yeni_sef_mesaji = MesajKaydi(oturum_id=oturum_id, rol="model", icerik=temiz_cevap)
        db.add(yeni_sef_mesaji)
        db.commit()
    
    db.close()
    return {"cevap": temiz_cevap}

@app.delete("/temizle/{oturum_id}")
async def sohbeti_sil(oturum_id: int):
    db = SessionLocal()
    db.query(MesajKaydi).filter(MesajKaydi.oturum_id == oturum_id).delete()
    db.query(SohbetOturumu).filter(SohbetOturumu.id == oturum_id).delete()
    db.commit()
    db.close()
    return {"mesaj": "Oturum silindi"}
@app.get("/kasa-kontrol")
async def kasa_kontrol():
    import os
    return {
        "GOOGLE_API_KEY_durumu": "Dolu ve okunuyor ✅" if os.getenv("GOOGLE_API_KEY") else "Kasa BOŞ ❌",
        "GEMINI_API_KEY_durumu": "Dolu ve okunuyor ✅" if os.getenv("GEMINI_API_KEY") else "Kasa BOŞ ❌"
    }