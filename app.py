import matplotlib
matplotlib.use('Agg')  # Fix GUI backend error

from flask import Flask, render_template, request, session
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'weather_secret_key'
API_KEY = '35170d8958741689c27754d0b1012321'  # Replace with your API key

def get_forecast_data(city=None, lat=None, lon=None):
    if city:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    elif lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        return None, None

    res = requests.get(url)
    if res.status_code != 200:
        return None, None

    data = res.json()
    forecast = data['list']
    current = forecast[0]
    times = [datetime.strptime(f['dt_txt'], "%Y-%m-%d %H:%M:%S") for f in forecast]
    temps = [f['main']['temp'] for f in forecast]
    humidity = [f['main']['humidity'] for f in forecast]

    # Plot with seaborn/matplotlib
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 5))
    plt.plot(times, temps, label='Temperature (°C)', marker='o')
    plt.plot(times, humidity, label='Humidity (%)', linestyle='--')
    plt.xlabel("Date/Time")
    plt.ylabel("Values")
    plt.title(f"5-Day Weather Forecast")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/weather_plot.png')
    plt.close()

    return forecast, current

@app.route('/', methods=['GET', 'POST'])
def index():
    city = None
    forecast = None
    current = None
    error = None

    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        city = request.form.get('city')
        lat = request.form.get('lat')
        lon = request.form.get('lon')

        if city:
            session['history'] = list(dict.fromkeys([city] + session['history']))[:5]
            forecast, current = get_forecast_data(city=city)
        elif lat and lon:
            forecast, current = get_forecast_data(lat=lat, lon=lon)
            city = current['name'] if current and 'name' in current else 'Current Location'
        else:
            error = "No city or location data received."

        if not forecast:
            error = "City not found or API error."

    return render_template(
        'index.html',
        city=city,
        image='weather_plot.png' if forecast else None,
        current=current,
        history=session.get('history', []),
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
