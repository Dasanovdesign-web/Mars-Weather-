import requests
import json
import time
import csv
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY")

# Формируем URL с использованием ключа из переменной окружения
URL = f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"

class MarsWeatherTerminal:
    def __init__(self):
        self.log_file = "mars_weather_history.csv"
        self._init_log()

    def _init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Sol", "Season", "Temp_Avg", "Temp_Min", "Temp_Max", "Wind_Speed", "Pressure"])

    def fetch_weather(self):
        if not API_KEY:
            print("[ОШИБКА] API ключ не найден. Проверьте файл .env")
            return None
            
        print(f"[{time.strftime('%H:%M:%S')}] Запрос данных с Марса...")
        try:
            response = requests.get(URL, timeout=15)
            if response.status_code == 200:
                return response.json()
            print(f"Ошибка API: {response.status_code}")
            return None
        except Exception as e:
            print(f"Ошибка сети: {e}")
            return None

    def process_data(self, data):
        if not data or "sol_keys" not in data or not data["sol_keys"]:
            print("Данные временно недоступны.")
            return

        latest_sol = data["sol_keys"][-1]
        weather = data[latest_sol]

        temp_av = weather.get("AT", {}).get("av", "Н/Д")
        temp_min = weather.get("AT", {}).get("mn", "Н/Д")
        temp_max = weather.get("AT", {}).get("mx", "Н/Д")
        season = weather.get("Season", "Н/Д")
        pressure = weather.get("PRE", {}).get("av", "Н/Д")
        wind_dir = weather.get("WD", {}).get("most_common", {}).get("compass_point", "Н/Д")
        wind_speed = weather.get("HWS", {}).get("av", "Н/Д")
        last_utc = weather.get("Last_UTC", "Н/Д")

        print("\n" + "="*45)
        print(f"   Отчет по Солу {latest_sol} | СЕЗОН: {season.upper()}")
        print("-" * 45)
        print(f"   Температура:")
        print(f"   Средняя: {temp_av} °C")
        print(f"   Диапазон: {temp_min} °C ... {temp_max} °C")
        print(f"   Ветер:")
        print(f"   Скорость: {wind_speed} m/s")
        print(f"   Направление: {wind_dir}")
        print(f"   Давление: {pressure} Pa")
        print(f"   Последняя запись (UTC): {last_utc}")
        print("=" * 45 + "\n")

        self._save_to_file(latest_sol, season, temp_av, temp_min, temp_max, wind_speed, pressure)

    def _save_to_file(self, sol, season, av, mn, mx, wind, press):
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), sol, season, av, mn, mx, wind, press])

    def run(self):
        data = self.fetch_weather()
        self.process_data(data)

if __name__ == "__main__":
    app = MarsWeatherTerminal()
    app.run()