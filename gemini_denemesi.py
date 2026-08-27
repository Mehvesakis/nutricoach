import requests
import base64

# 1. VIP Kartın
API_KEY = "API_ANAHTARI_BURAYA_GELECEK"

# 2. Şefin adresi
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"

# 3. Fotoğrafı Base64 diline çeviriyoruz
resim_yolu = "tabak.png"
with open(resim_yolu, "rb") as resim_dosyasi:
    resim_sifresi = base64.b64encode(resim_dosyasi.read()).decode("utf-8")

# 4. KULLANICI SORUSU (Sıradan, basit bir soru)
soru = "Bu fotoğraftaki yiyecekleri analiz et, kalorilerini hesapla."

# 5. SİSTEM KOMUTU (Senin Mühendis Olarak Yazdığın Gizli Kurallar)
sistem_komutu = """Sen profesyonel bir diyetisyensin.
1. Fotoğraftaki her malzemeyi gramajıyla tahmin et.
2. Toplam kalori ve makro (protein, karbonhidrat, yağ) değerlerini hesapla.
3. EĞER fotoğrafta yemek yoksa 'Gecersiz_Gorsel' hatası fırlat.
4. CEVABINI SADECE JSON FORMATINDA VER. Metin, selamlama veya açıklama KESİNLİKLE kullanma."""

# 6. Yeni Sipariş Tepsisi (Şefe hem kuralları hem soruyu veriyoruz)
siparis_tepsisi = {
    "system_instruction": {
        "parts": [{"text": sistem_komutu}]
    },
    "contents": [{
        "parts": [
            {"text": soru},
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": resim_sifresi
                }
            }
        ]
    }]
}

print("Uzman Diyetisyen AI fotoğrafı inceliyor, lütfen bekle...\n")

cevap = requests.post(url, json=siparis_tepsisi)
veri = cevap.json()

# 7. Kurşun Geçirmez Kalkanımız
if 'error' in veri:
    print("--- 🚨 MUTFAKTAN HATA MESAJI GELDİ 🚨 ---")
    print(veri['error']['message'])
else:
    akilli_cevap = veri['candidates'][0]['content']['parts'][0]['text']
    print("--- 📸 PROFESYONEL AI DİYETİSYEN SONUCU ---")
    print(akilli_cevap)
    print("-----------------------------------------")