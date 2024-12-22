import pandas as pd
from sqlalchemy import create_engine
import time

# Database configuration
DB_USER = 'data_ingestor'
DB_PASSWORD = 'Adrianj7769!'  # Replace with your actual password
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'rpi_algo'

# Create SQLAlchemy engine
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)


def fetch_latest_candles(symbol, limit=1000):
    query = f"""
    SELECT * FROM candle_data
    WHERE EventSymbol = '{symbol}'
    ORDER BY EventTime DESC
    LIMIT {limit};
    """
    df = pd.read_sql(query, engine)
    df = df.sort_values('EventTime')  # Ensure data is sorted by time
    return df

def calculate_moving_average(df, window=10):
    df['Moving_Avg_10'] = df['Close'].rolling(window=window).mean()
    return df

def main():
    symbol = 'IBM{=d}'  # Replace with your desired symbol
    while True:
        df = fetch_latest_candles(symbol, 1000)
        df_with_ma = calculate_moving_average(df, 10)
        latest_entry = df_with_ma.iloc[-1]
        print(f"Time: {latest_entry['EventTime']}, Close: {latest_entry['Close']}, 10-MA: {latest_entry['Moving_Avg_10']}")
        time.sleep(5)  # Wait for 5 seconds before fetching new data

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Real-time calculations stopped by user.")
