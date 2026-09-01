# 🍏 NutriCoach - AI Beslenme ve Diyet Koçu

NutriCoach, kullanıcılarına kişiselleştirilmiş beslenme önerileri, antrenman sonrası öğün planlamaları ve diyet takibi sunan, yapay zeka destekli full-stack bir web uygulamasıdır. 

🚀 **[CANLI DEMO İÇİN TIKLAYIN](https://nutricoach-ykke.vercel.app)**

## 🌟 Öne Çıkan Özellikler
* **Özelleştirilmiş Yapay Zeka:** Google Gemini API ve özel prompt mühendisliği ile geliştirilmiş, beslenme kurallarına sadık sanal koç.
* **Oturum Yönetimi:** Geçmiş sohbetleri hatırlayan ve farklı konular için yeni sekmeler açabilen akıllı hafıza.
* **Modern Arayüz:** React ve Vite ile geliştirilmiş, hızlı ve duyarlı (responsive) tasarım.
* **Bulut Mimarisi:** İstemci ve sunucu olarak ayrıştırılmış, Vercel ve Render üzerinde 7/24 çalışan bağımsız sistem.

## 🛠️ Kullanılan Teknolojiler
* **Yapay Zeka:** Google Gemini 1.5 Flash, Prompt Engineering
* **Backend:** Python, FastAPI, SQLite, SQLAlchemy, Uvicorn
* **Frontend:** React, Vite, React-Markdown
* **Deployment:** Vercel (Frontend), Render (Backend)

## ⚙️ Kurulum (Geliştiriciler İçin)
Projeyi kendi bilgisayarınızda çalıştırmak için:
1. Depoyu klonlayın: `git clone https://github.com/Mehvesakis/nutricoach.git`
2. Backend bağımlılıklarını kurun: `pip install -r requirements.txt`
3. Frontend bağımlılıklarını kurun: `cd kalorisi-arayuz && npm install`
4. Backend için bir `.env` dosyası oluşturup `GOOGLE_API_KEY` değerinizi ekleyin.
