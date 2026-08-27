# 🍏 NutriCoach AI - Full-Stack Yapay Zeka Beslenme Koçu

NutriCoach, sporcular ve sağlıklı yaşam tutkunları için geliştirilmiş, RAG (Retrieval-Augmented Generation) destekli kişiselleştirilmiş bir yapay zeka asistanıdır. Standart bir kalori sayacının ötesine geçerek kuvvet antrenmanları ve kas onarımı için nokta atışı makro tavsiyeleri sunar.

## 🚀 Öne Çıkan Özellikler
* **Çoklu Oturum (Multi-Session) Mimarisi:** Kullanıcıların sohbet geçmişini klasörler halinde (oturum bazlı) saklar.
* **Akıllı RAG Sistemi:** Sisteme yüklenen özel diyet ve antrenman kuralları veritabanı üzerinden, halüsinasyondan uzak ve amaca yönelik yanıtlar üretir.
* **Optimistic UI:** Silme ve yeni sohbet açma işlemlerinde veritabanını beklemeden anında tepki veren akıcı arayüz.
* **Dinamik Başlıklandırma:** Kullanıcının attığı ilk mesaja göre sohbet oturumunun başlığını yapay zeka ile otomatik belirler.

## 🛠️ Teknoloji Yığını (Tech Stack)
* **Frontend:** React, React-Markdown, Modern Soft-UI CSS
* **Backend:** Python, FastAPI, SQLAlchemy
* **Veritabanı:** SQLite (İlişkisel oturum ve mesaj tabloları)
* **Yapay Zeka:** Google Gemini 3.6 Flash API

## 💻 Kurulum
Projeyi kendi bilgisayarınızda çalıştırmak için:
1. Arka uç bağımlılıklarını kurun ve `api_sunucusu.py` dosyasını çalıştırın (Port 8000).
2. Ön yüz klasörüne (`kalorisi-arayuz`) girip `npm install` ve ardından `npm run dev` komutlarını çalıştırın.