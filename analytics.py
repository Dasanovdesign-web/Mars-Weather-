import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_mars_dashboard(file_path="mars_weather_history.csv"):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print("База данных пуста.")
            return

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values('Timestamp')

        plt.style.use('dark_background')
        # Создаем сетку
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        fig.patch.set_facecolor('#1F1F1F')

        # ГРАФИК 1:  Температура 
        ax1.set_facecolor('#1F1F1F')
        ax1.plot(df['Timestamp'], df['Temp_Avg'], color='#FACE0C', label='Средняя T°', linewidth=2, marker='o')
        ax1.fill_between(df['Timestamp'], df['Temp_Min'].astype(float), df['Temp_Max'].astype(float), 
                         color='#FACE0C', alpha=0.1, label='Диапазон')
        ax1.set_ylabel('Градусы Цельсия (°C)', color='white')
        ax1.legend(loc='upper left')
        ax1.set_title('МАРСИАНСКИЙ ДАШБОРД: ТЕМПЕРАТУРА И ДАВЛЕНИЕ', fontsize=14, pad=20)

        # --- ГРАФИК 2: Давление ---
        ax2.set_facecolor('#1F1F1F')
        ax2.plot(df['Timestamp'], df['Pressure'], color='#00AD20', label='Давление (Pa)', linewidth=2, linestyle='--')
        ax2.set_ylabel('Паскали (Pa)', color='white')
        ax2.set_xlabel('Дата и время замера (UTC)', color='white')
        ax2.legend(loc='upper left')

        # Настройка формата даты (только для нижнего графика из-за sharex=True)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
        plt.xticks(rotation=45)
        
        for ax in [ax1, ax2]:
            ax.grid(True, linestyle='--', alpha=0.2)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Ошибка визуализации: {e}")

if __name__ == "__main__":
    plot_mars_dashboard()