from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 1. VIP Kartımız
api_anahtari = "API_ANAHTARI_BURAYA_GELECEK"

# 2. Şefimizi Hazırlıyoruz
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_anahtari
)

# 3. KENDİ VERİMİZİ (RAG) OKUYORUZ
# diyet_kurallari.txt dosyasını açıp içindeki tüm metni 'kurallar' değişkenine kopyalıyoruz.
with open("diyet_kurallari.txt", "r", encoding="utf-8") as dosya:
    kurallar = dosya.read()

# 4. SİSTEM MESAJI (Kurallar + Karakter)
# Şefe hem kim olduğunu hem de uyması gereken katı kuralları veriyoruz.
sistem_talimati = f"""Sen Kalorisi uygulamasının zeki ve hafızası çok güçlü diyetisyenisin.
Aşağıdaki kuralların DIŞINA ASLA ÇIKMAYACAKSIN. Eğer sana sorulan soru kurallara aykırıysa, kesin bir dille reddet:

--- KURALLAR BAŞLANGICI ---
{kurallar}
--- KURALLAR BİTİŞİ ---
"""

# Hafızayı başlatıyoruz ve ilk sıraya bu değişmez yasaları koyuyoruz
sohbet_gecmisi = [
    SystemMessage(content=sistem_talimati)
]

# 5. BİRİNCİ TUR: Hem Kuralları Hem Hafızayı Test Ediyoruz
print("--- 1. MESAJ GÖNDERİLİYOR ---")
# Senin günlük rutininden ve txt dosyasındaki muhtemel bir yasaktan (örneğin akşam geç saatte ağır yemek) yola çıkarak bir test yapalım.
mesaj_1 = "Merhaba şef, benim adım Mehveş. Sabah yulaf ve chia tohumlu kase yedim. Şimdi saat akşam 21:00, sence kocaman bir iskender yiyebilir miyim?"
sohbet_gecmisi.append(HumanMessage(content=mesaj_1)) 

cevap_1 = llm.invoke(sohbet_gecmisi) 
temiz_cevap_1 = cevap_1.content[0]['text'] # Dünkü muhteşem cımbızlama taktiğimiz!

sohbet_gecmisi.append(AIMessage(content=temiz_cevap_1))
print("Şefin Cevabı:\n", temiz_cevap_1)

print("\n" + "="*50 + "\n")

# 6. İKİNCİ TUR: Hafıza Kontrolü
print("--- 2. MESAJ GÖNDERİLİYOR ---")
mesaj_2 = "Peki benim adım neydi ve sabah ne yemiştim?"
sohbet_gecmisi.append(HumanMessage(content=mesaj_2)) 

cevap_2 = llm.invoke(sohbet_gecmisi) 
temiz_cevap_2 = cevap_2.content[0]['text']

print("Şefin Cevabı:\n", temiz_cevap_2)