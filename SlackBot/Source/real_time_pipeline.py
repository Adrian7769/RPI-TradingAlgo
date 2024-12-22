

import asyncio
import websockets
import json
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from collections import deque
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------ Configuration ------------------ #

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')  
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# WebSocket configuration
WS_URL = 'wss://api.tastytrade.com/stream'  # Replace with actual WebSocket URL
API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key

# Batch configuration
BATCH_SIZE = 500  # Number of records per batch insert
BATCH_INTERVAL = 30  # Seconds between batch inserts

# Logging configuration
logging.basicConfig(
    filename='data_ingestion.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# --------------------------------------------------- #

# Create SQLAlchemy engine
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_size=20,
    max_overflow=0
)

# Initialize a deque to store incoming data
data_queue = deque()

async def parse_timestamp(ts_str):
    """
    Parses timestamp strings into datetime objects.
    Format: 'YYYYMMDD-HHMMSS.mmm-TZ'
    Example: '20210506-200000.000-0400'
    """
    try:
        return datetime.strptime(ts_str, '%Y%m%d-%H%M%S.%f%z')
    except ValueError as e:
        logging.error(f"Timestamp parsing error: {e} for {ts_str}")
        return None

async def process_candle(candle_data):
    """
    Parses a single candle entry and appends it to the queue.
    """
    if candle_data[0] != 'Candle':
        return  # Ignore non-candle data

    fields = candle_data[1]
    if len(fields) < 15:
        logging.warning(f"Incomplete candle data: {fields}")
        return  # Incomplete data

    # Extract fields
    event_symbol = fields[0]
    event_time_str = fields[1]
    time_str = fields[2]
    sequence = fields[3]
    count = fields[4]
    open_price = fields[5]
    high_price = fields[6]
    low_price = fields[7]
    close_price = fields[8]
    volume = fields[9]
    vwap = fields[10]
    bid_volume = fields[11]
    ask_volume = fields[12]
    imp_volatility = fields[13]
    open_interest = fields[14] if len(fields) > 14 else None
    event_flags = fields[15] if len(fields) > 15 else None

    # Parse timestamps
    event_time = await parse_timestamp(event_time_str)
    time = await parse_timestamp(time_str)

    # Handle 'NaN' strings by converting them to None
    open_interest = float(open_interest) if open_interest not in (None, 'NaN') else None

    # Create a dictionary for the row
    row = {
        'EventSymbol': event_symbol,
        'EventTime': event_time,
        'Time': time,
        'Sequence': sequence,
        'Count': count,
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Volume': volume,
        'VWAP': vwap,
        'BidVolume': bid_volume,
        'AskVolume': ask_volume,
        'ImpVolatility': imp_volatility,
        'OpenInterest': open_interest,
        'EventFlags': event_flags
    }

    # Append to queue
    data_queue.append(row)

    # Log the event
    logging.info(f"Queued candle for {event_symbol} at {event_time}")

    # Check if batch size is reached
    if len(data_queue) >= BATCH_SIZE:
        await insert_batch()

async def insert_batch():
    """
    Inserts a batch of candles from the queue into the database.
    """
    if not data_queue:
        return

    # Convert deque to list and then to DataFrame
    data_list = list(data_queue)
    df = pd.DataFrame(data_list)
    data_queue.clear()

    # Handle missing data
    df['OpenInterest'] = pd.to_numeric(df['OpenInterest'], errors='coerce')
    df['EventFlags'] = df['EventFlags'].fillna('')

    # Insert into PostgreSQL
    try:
        df.to_sql('candle_data', engine, if_exists='append', index=False, method='multi')
        logging.info(f"Inserted batch of {len(df)} candles into the database.")
    except Exception as e:
        logging.error(f"Error inserting batch into database: {e}")
        # Re-queue the data for retry
        for _, row in df.iterrows():
            data_queue.append(row.to_dict())

async def batch_inserter():
    """
    Periodically inserts batches of data into the database.
    """
    while True:
        await asyncio.sleep(BATCH_INTERVAL)
        await insert_batch()

async def listen():
    """
    Connects to the WebSocket and listens for incoming candle data.
    """
    async with websockets.connect(WS_URL) as websocket:
        # Authenticate if required
        auth_message = {
            "action": "authenticate",
            "api_key": API_KEY
        }
        await websocket.send(json.dumps(auth_message))
        logging.info("Sent authentication message.")

        # Start the batch inserter task
        asyncio.create_task(batch_inserter())

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                # Process only FEED_DATA type messages
                if data.get('type') == 'FEED_DATA':
                    events = data.get('data', [])
                    if events and isinstance(events, list):
                        for candle in events:
                            await process_candle(candle)

            except websockets.exceptions.ConnectionClosed:
                logging.warning("WebSocket connection closed. Attempting to reconnect in 5 seconds...")
                await asyncio.sleep(5)
                asyncio.create_task(listen())
                break
            except Exception as e:
                logging.error(f"Error processing message: {e}")

# Entry point
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(listen())
    except KeyboardInterrupt:
        logging.info("Data ingestion stopped by user.")
