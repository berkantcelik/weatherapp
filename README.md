# ☀️ Weather & Outfit Advisor

This project is a Flask-based web application that takes a location input from the user, queries current weather conditions, and provides **outfit suggestions** based on factors like temperature, wind, humidity, and UV index.

## 🚀 Features

* **Real-Time Weather:** Fetches up-to-date data via WeatherAPI.com.
* **Smart Algorithm:** Bases recommendations on "Perceived Temperature" by calculating Wind Chill and Heat Index, not just the thermometer reading.
* **Comprehensive Suggestions:**
    * Core outfit recommendations (Coat, T-shirt, etc.)
    * Accessory advice (Umbrella, Sunglasses, Gloves)
    * UV protection alerts
* **User-Friendly Interface:** Clean and simple HTML/CSS design.

## 📂 Project Structure

It is **important** to organize the files in the following structure for Flask to work correctly:

```text
weather-app/
├── app.py              # Python application file
├── templates/
│   └── index.html      # HTML template file
└── README.md           # This file
```

> **Note:** The `index.html` file must be placed inside a folder named `templates`.

## 🛠️ Installation

### 1. Requirements
Python 3.x must be installed on your computer.

### 2. Installing Libraries
Run the following command in your terminal or command line to install the necessary Python libraries:

```bash
pip install flask requests
```

### 3. Getting an API Key
This application uses the [WeatherAPI.com](https://www.weatherapi.com/) service.
1.  Go to the site and create a free account.
2.  Get your own API Key.

## ⚙️ Configuration (Important)

For security reasons, the API key is not written directly into the code; it is set as an Environment Variable. You must define your key before running the application.

**Windows (CMD):**
```cmd
set WEATHER_API_KEY=Your_API_Key_Here
```

**Windows (PowerShell):**
```powershell
$env:WEATHER_API_KEY="Your_API_Key_Here"
```

**Mac / Linux (Terminal):**
```bash
export WEATHER_API_KEY=Your_API_Key_Here
```

## ▶️ Running the App

After configuring the settings, start the application:

```bash
python app.py
```

You will see the following output in the terminal:
`Running on http://127.0.0.1:5000`

Open your browser and go to `http://127.0.0.1:5000`.

## 📝 Usage

1.  Enter a city name (e.g., `London`), zip code, or latitude/longitude into the search box.
2.  Click the **Get Weather** button.
3.  The application will display the weather conditions and detailed advice on what to wear for the day.

## 🛡️ Error Handling

* **API Key Error:** If the API key is not defined, you will see a "FATAL ERROR" warning in the console.
* **City Not Found:** If an invalid location is entered, an error message will appear on the screen.

