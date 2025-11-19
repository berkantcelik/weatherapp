import requests

API_KEY = "5f7d622d367648d686a235233251811"
BASE_URL = "http://api.weatherapi.com/v1/current.json"
LOCATION = input("Şehir adı veya Posta Kodu girin: ") 

# 1. Parametreler sözlüğü
params = {
    'key': API_KEY,
    'q': LOCATION,
    'aqi': 'no',
    'lang': 'tr' # Türkçe açıklama almak için ekledik (isteğe bağlı)
}

# 2. GET isteği
response = requests.get(BASE_URL, params=params)

# --- Aşama 5: Yanıtı İşleme ---

if response.status_code == 200:
    # 1. JSON verisini Python sözlüğüne dönüştür
    data = response.json()
    
    # 2. İhtiyacımız olan bilgileri JSON yapısından çıkarma
    try:
        # Konum Bilgileri
        sehir = data['location']['name']
        ulke = data['location']['country']
        
        # Hava Durumu Bilgileri (current anahtarının altında)
        sicaklik = data['current']['temp_c'] # Santigrat derece
        durum = data['current']['condition']['text'] # Türkçe hava durumu açıklaması
        ruzgar = data['current']['wind_kph'] # Rüzgar hızı (km/s)
        nem = data['current']['humidity'] # Nem yüzdesi
        
        # --- Aşama 6: Çıktıyı Kullanıcıya Gösterme ---
        print("\n--- Güncel Hava Durumu Raporu ---")
        print(f"Konum: **{sehir}, {ulke}**")
        print(f"Sıcaklık: **{sicaklik}°C**")
        print(f"Durum: **{durum}**")
        print(f"Rüzgar Hızı: **{ruzgar} km/s**")
        print(f"Nem Oranı: **%{nem}**")
        print("----------------------------------")
        # Verilerinizi ondalıklı sayı (float) olarak kabul ettiğimizden, 
# karşılaştırma yaparken int() kullanmaya gerek yoktur.

        if sicaklik >= 30 and nem > 70:
            # Aşırı sıcak ve bunaltıcı (Yüksek sıcaklık + Yüksek nem)
            print("🔥 BOĞUCU HAVA: Çok sıcak ve nemli. Mümkünse dışarı çıkmayın. Çıksanız bile en hafif, nefes alan kumaşları (keten, pamuk) ve bol kıyafetleri tercih edin.")
            
        elif sicaklik >= 30 and ruzgar > 25:
            # Sıcak ama rüzgarlı
            print("💨 SICAK RÜZGAR: Hava sıcak olsa da rüzgar serinletebilir. İnce ve açık renkli kıyafetler giyin. Rüzgarın toz taşıma ihtimaline karşı gözlük takmayı düşünebilirsiniz.")
            
        elif sicaklik >= 25:
            # Yazlık ideal hava (25-30 arası)
            print("☀️ YAZ HAVASI: Şort, tişört gibi ince ve rahat yazlık kıyafetler idealdir. Güneş kremi kullanmayı unutmayın.")
            
        elif sicaklik >= 18 and ruzgar < 15:
            # Ilık ve sakin (18-25 arası)
            print("🍃 İLKBAHAR/SONBAHAR: Gün ortası için ince bir üst yeterli olabilir. Akşam serinliği için yanınıza ince bir hırka veya uzun kollu gömlek alın.")
            
        elif sicaklik >= 10 and ruzgar > 20:
            # Rüzgarın hissedilen sıcaklığı düşürdüğü serin hava
            print("💨 SERİN VE RÜZGARLI: Rüzgar soğuk hissettirecektir. Rüzgar geçirmeyen (windbreaker) bir ceket veya mont ile atkı/bere gibi aksesuarları kullanın.")
            
        elif sicaklik >= 5:
            # Soğuk ama dondurucu olmayan (5-10 arası)
            print("🧥 SOĞUK HAVA: Kalın bir ceket veya ince mont giyin. Kat kat giyinmek (termal içlik, tişört, kazak) en iyisidir. Kapalı ayakkabılar tercih edin.")
            
        elif sicaklik >= 0 and sicaklik < 5:
            # Dondurucuya yakın (0-5 arası)
            print("🧤 BUZ GİBİ HAVA: Kalın kışlık mont, bere, eldiven ve atkı mutlaka kullanın. Termal içlik şiddetle önerilir. Donma riski olan yüzeylere dikkat edin.")
            
        else: # sicaklik < 0
            # Sıfırın altındaki dereceler
            print("❄️ DONUYOR: Hava çok soğuk, dikkatli olun! En kalın kışlık kıyafetlerinizi, kabanlarınızı giyin. Maruz kalınan cilt yüzeyini koruyun ve dışarıda kalma sürenizi sınırlayın.")
    except KeyError as e:
        # JSON yapısında beklenen bir anahtarın bulunamaması hatası
        print(f"Hata: API yanıtında beklenen veri bulunamadı. Eksik anahtar: {e}")
        
else:
    # Hata durumunu yönetme (400, 403, 404 gibi HTTP kodları)
    print(f"\nHata: Hava durumu verisi alınamadı. HTTP Kodu: {response.status_code}")
    
    # API'den gelen hata mesajını göstermeyi deneyelim (örneğin, yanlış API anahtarı veya şehir adı)
    try:
        error_data = response.json()
        if 'error' in error_data:
            print(f"API Mesajı: {error_data['error']['message']}")
    except:
        print("API'den detaylı hata mesajı alınamadı.")

