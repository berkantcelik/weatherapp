from flask import Flask, render_template, request
import requests
import os

# --- CONFIGURATION ---
# API Key is securely read from environment variables.
API_KEY = os.environ.get("WEATHER_API_KEY") 
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Check for API Key at startup
if not API_KEY:
    # In a real production environment, you would log this error and handle it more gracefully.
    print("FATAL ERROR: WEATHER_API_KEY environment variable is not set.")

app = Flask(__name__)

# --- BUSINESS LOGIC ---

def get_outfit_suggestion(temp_c, condition_text, wind_kph, humidity, uv_index=0):
    """
    Provides a comprehensive clothing recommendation based on various weather factors,
    including wind chill and precipitation.
    """
    
    # 1. Calculate Perceived Temperature (Hissedilen Sicaklik)
    wind_chill_effect = 0
    heat_index_effect = 0
    
    if temp_c < 10 and wind_kph > 20:
        # Wind Chill effect for cold temperatures
        wind_chill_effect = (wind_kph - 20) * 0.35 
    elif temp_c > 25 and humidity > 60:
        # Heat Index effect for hot and humid conditions
        heat_index_effect = (humidity - 60) * 0.15 * (temp_c / 30) 
        
    perceived_temp = temp_c - wind_chill_effect + heat_index_effect
    
    
    # 2. Accessory and Protection Check
    accessory_advice = []
    condition_lower = condition_text.lower()
    
    # Precipitation Advice
    if 'rain' in condition_lower or 'drizzle' in condition_lower or 'shower' in condition_lower:
        accessory_advice.append("Waterproof jacket and umbrella required.")
    elif 'snow' in condition_lower or 'sleet' in condition_lower or 'blizzard' in condition_lower:
        accessory_advice.append("Snow boots, heavy scarf, and gloves are a must.")
    
    # UV and Sun Protection
    if uv_index >= 6 and perceived_temp >= 20:
        accessory_advice.append("High UV Alert! Hat and SPF 30+ sunscreen are mandatory.")
    elif uv_index >= 3 and perceived_temp >= 25:
        accessory_advice.append("Don't forget sunglasses and apply sunscreen.")

    # Wind Advice
    if perceived_temp < 15 and wind_kph > 30:
        accessory_advice.append("Wear wind-blocking outer layers.")
        
    
    # 3. Core Clothing Recommendation (Based on Perceived Temperature)
    
    if perceived_temp >= 32:
        core_outfit = "EXTREME HEAT: Lightest, breathable fabrics (linen, cotton), and loose-fitting clothes. Stay hydrated."
    elif perceived_temp >= 26:
        core_outfit = "HOT SUMMER: Shorts, skirts, and t-shirts. Light-colored clothing is recommended."
    elif perceived_temp >= 20:
        core_outfit = "MILD DAY: Short sleeves for midday, but carry a light cardigan or jacket for the evening (layering is key)."
    elif perceived_temp >= 12:
        core_outfit = "COOL SPRING/AUTUMN: Long sleeves and a medium-weight jacket (denim or trench coat). Closed shoes."
    elif perceived_temp >= 5:
        core_outfit = "COLD START: Heavy coat or winter jacket, consider wearing a hat/scarf. Waterproof footwear."
    elif perceived_temp >= 0:
        core_outfit = "FREEZING POINT: Heavy winter coat, thermal layers underneath, gloves, and a wool hat are essential."
    else: # perceived_temp < 0
        core_outfit = "DANGEROUSLY COLD: Double-layer thermals and thickest outerwear. Limit exposed skin and minimize time outdoors."
    
    
    # 4. Final Output Formatting
    
    final_suggestion = f"Perceived Temperature: {perceived_temp:.1f}°C\n"
    final_suggestion += f"CORE OUTFIT: {core_outfit}\n"
    
    if accessory_advice:
        final_suggestion += "\nACCESSORY ADVICE:\n" + "\n".join(accessory_advice)
    
    return final_suggestion

# --- FLASK ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    suggestion = None
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        location_name = request.form.get('location') 
        
        # Ensure API Key is set before making the request
        if location_name and API_KEY:
            params = {
                'key': API_KEY,
                'q': location_name,
                'aqi': 'no',
                'lang': 'en' # Setting language to English for consistency
            }
            
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status() # Check for HTTP errors (4xx/5xx)
                data = response.json()
                
                # Extract Data (Ensure your API call includes UV data)
                temp_c = data['current']['temp_c']
                condition_text = data['current']['condition']['text']
                wind_kph = data['current']['wind_kph']
                humidity = data['current']['humidity']
                uv_index = data['current']['uv'] 
                
                # Package data for the template
                weather_data = {
                    'city': data['location']['name'],
                    'country': data['location']['country'],
                    'temp_c': temp_c,
                    'condition': condition_text,
                    'wind_kph': wind_kph,
                    'humidity': humidity,
                    'uv_index': uv_index
                }
                
                # Get the detailed suggestion
                suggestion = get_outfit_suggestion(temp_c, condition_text, wind_kph, humidity, uv_index)

            except requests.exceptions.HTTPError:
                weather_data = {'error': 'Could not find weather data for the entered location.'}
            except requests.exceptions.RequestException:
                weather_data = {'error': 'Failed to connect to the weather API server.'}
            except KeyError:
                weather_data = {'error': 'API response format is missing expected data.'}
        
        elif not API_KEY:
             weather_data = {'error': 'Server Error: API Key is not configured.'}

    # Render the HTML template
    return render_template('index.html', weather=weather_data, suggestion=suggestion)

# This part is used by Render/Gunicorn to start the application
if __name__ == '__main__':
    app.run(debug=True)