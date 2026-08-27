import requests 

print("API'nin kapısını çalıyoruz, veri bekleniyor...\n")

# Bu kez bizi engellemeyecek, testler için özel yapılmış bir API kullanıyoruz
url = "https://dummyjson.com/products/1"

cevap = requests.get(url)

# Gelen tabağı JSON formatında açıyoruz
veri = cevap.json()

# İçinden istediğimiz parçaları cımbızlıyoruz
urun_adi = veri['title']
fiyat = veri['price']
kategori = veri['category']
# Dünkü cımbızladıklarımız
urun_adi = veri['title']
fiyat = veri['price']
kategori = veri['category']

# BURADAN İTİBAREN SEN EKLİYORSUN:
# Yeni verileri cımbızlıyoruz
stok_durumu = veri['stock']
aciklama = veri['description']

print("--- SONUÇ ---")
print(f"Ürün Adı: {urun_adi}")
print(f"Kategori: {kategori}")
print(f"Fiyatı: {fiyat} $")
# Bu print'leri de ekrana yazdırıyoruz
print(f"Stok Adedi: {stok_durumu}")
print(f"Açıklama: {aciklama}")
print("-------------")