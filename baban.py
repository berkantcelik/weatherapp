from flask import Flask, render_template, request
import requests
import os # Ortam değişkenlerini okumak için

# --- SABİTLERİN TANIMLANMASI ---
# API Anahtarı doğrudan koda yazılmaz, ortam değişkeninden (Render'da tanımladığınız) okunur.
API_KEY = os.environ.get("WEATHER_API_KEY") 
BASE_URL = "http://api.weatherapi.com/v1/current.json"

if not API_KEY:
    # Eğer ortam değişkeni ayarlanmamışsa, program çalışmaya devam edemez.
    # Bu kontrolü yerel geliştirme sırasında da yapın.
    print("HATA: WEATHER_API_KEY ortam değişkeni ayarlanmadı.")
    # Production ortamında (Render) bu bir 500 hatasına neden olur.

# Flask uygulamasını başlatma
app = Flask(__name__)

# Kıyafet önerisi mantığı (Ayrı bir fonksiyon olarak düzenlendi)
def get_outfit_suggestion(sicaklik, ruzgar, nem):
    """Sıcaklık, rüzgar ve neme göre kıyafet önerisi döndürür."""
    if sicaklik >= 30 and nem > 70:
        return "🔥 BOĞUCU HAVA: Çok sıcak ve nemli. En hafif, nefes alan kumaşları (keten, pamuk) ve bol kıyafetleri tercih edin."
    elif sicaklik >= 30 and ruzgar > 25:
        return "💨 SICAK RÜZGAR: Hava sıcak olsa da rüzgar serinletebilir. İnce ve açık renkli kıyafetler giyin."
    elif sicaklik >= 25:
        return "☀️ YAZ HAVASI: Şort, tişört gibi ince ve rahat yazlık kıyafetler idealdir. Güneş kremi kullanmayı unutmayın."
    elif sicaklik >= 18 and ruzgar < 15:
        return "🍃 İLKBAHAR/SONBAHAR: Gün ortası için ince bir üst yeterli olabilir. Akşam serinliği için yanınıza ince bir hırka veya uzun kollu gömlek alın."
    elif sicaklik >= 10 and ruzgar > 20:
        return "💨 SERİN VE RÜZGARLI: Rüzgar soğuk hissettirecektir. Rüzgar geçirmeyen (windbreaker) bir ceket veya mont kullanın."
    elif sicaklik >= 5:
        return "🧥 SOĞUK HAVA: Kalın bir ceket veya ince mont giyin. Kat kat giyinmek en iyisidir."
    elif sicaklik >= 0: # 0 dahil, 5 hariç
        return "🧤 BUZ GİBİ HAVA: Kalın kışlık mont, bere, eldiven ve atkı mutlaka kullanın. Termal içlik önerilir."
    else: # sicaklik < 0
        return "❄️ DONUYOR: Hava çok soğuk, dikkatli olun! En kalın kışlık kıyafetlerinizi, kabanlarınızı giyin."


# Ana Rota Fonksiyonu: Web isteği burada işlenir
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    suggestion = None
    
    # Kullanıcıdan POST isteği (form gönderimi) geldiyse
    if request.method == 'POST':
        location_name = request.form.get('location') 
        
        if location_name and API_KEY:
            params = {
                'key': API_KEY,
                'q': location_name,
                'aqi': 'no',
                'lang': 'tr'
            }
            
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status() # HTTP hatalarını (4xx/5xx) kontrol eder
                data = response.json()
                
                # Verileri Çıkarma
                sicaklik = data['current']['temp_c']
                ruzgar = data['current']['wind_kph']
                nem = data['current']['humidity']
                
                # Web arayüzüne göndermek üzere verileri topla
                weather_data = {
                    'sehir': data['location']['name'],
                    'ulke': data['location']['country'],
                    'sicaklik': sicaklik,
                    'durum': data['current']['condition']['text'],
                    'ruzgar': ruzgar,
                    'nem': nem,
                }
                
                # Kıyafet önerisini al
                suggestion = get_outfit_suggestion(sicaklik, ruzgar, nem)

            except requests.exceptions.HTTPError:
                weather_data = {'error': 'Girilen konum için hava durumu verisi bulunamadı.'}
            except requests.exceptions.RequestException:
                weather_data = {'error': 'API sunucusuyla bağlantı kurulamadı.'}
            except KeyError:
                weather_data = {'error': 'API yanıtı beklenenden farklı bir formatta.'}
        
        elif not API_KEY:
             weather_data = {'error': 'Sunucu Hatası: API Anahtarı ayarlanmamış.'}

    # index.html şablonunu göster ve verileri (varsa) ona gönder.
    return render_template('index.html', weather=weather_data, suggestion=suggestion)

# Uygulamanın başlatılması için gerekli kısım
if __name__ == '__main__':
    # Sadece yerel testler için, Render bu kısmı kullanmaz.
    app.run(debug=True)