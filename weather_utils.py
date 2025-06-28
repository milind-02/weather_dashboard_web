import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

API_KEY = '35170d8958741689c27754d0b1012321'  # Replace with your real API key

def fetch_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()

    weather_data = {
        "datetime": [],
        "temperature": [],
        "humidity": [],
        "description": []
    }

    for entry in data['list']:
        weather_data["datetime"].append(entry["dt_txt"])
        weather_data["temperature"].append(entry["main"]["temp"])
        weather_data["humidity"].append(entry["main"]["humidity"])
        weather_data["description"].append(entry["weather"][0]["main"])

    return pd.DataFrame(weather_data)

def plot_dashboard(df, city):
    sns.set(style="darkgrid")
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    sns.lineplot(x='datetime', y='temperature', data=df, ax=axes[0], color='orange')
    axes[0].set_title(f'Temperature Variation - {city}')
    axes[0].tick_params(axis='x', rotation=45)

    sns.lineplot(x='datetime', y='humidity', data=df, ax=axes[1], color='blue')
    axes[1].set_title(f'Humidity Levels - {city}')
    axes[1].tick_params(axis='x', rotation=45)

    sns.countplot(x='description', data=df, ax=axes[2], palette='Set2')
    axes[2].set_title(f'Weather Conditions Frequency - {city}')

    plt.tight_layout()
    img_path = os.path.join('static', 'weather_plot.png')
    plt.savefig(img_path)
    plt.close()
    return img_path
