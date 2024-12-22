import os
import asyncio
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from tastytrade import Session, DXLinkStreamer
from tastytrade.dxfeed import Candle

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

USERNAME = os.getenv("TASTY_USER")
PASSWORD = os.getenv("TASTY_PASS")

async def fetch_historical_candles(symbols, interval, start_time, end_time, extended_trading_hours=False):
    """
    Fetch historical candle data for given symbols.

    :param symbols: List of stock symbols (e.g., ['AAPL', 'MSFT'])
    :param interval: Candle interval (e.g., '5m', '1h')
    :param start_time: Start time as timezone-aware datetime object
    :param end_time: End time as timezone-aware datetime object
    :param extended_trading_hours: Include extended trading hours
    :return: Dictionary with symbols as keys and lists of candle data as values
    """
    # Initialize session
    session = Session(login=USERNAME, password=PASSWORD)
    
    # Initialize data storage
    candles_data = {symbol: [] for symbol in symbols}
    
    async with DXLinkStreamer(session) as streamer:
        # Subscribe to candle data
        await streamer.subscribe_candle(
            symbols=symbols,
            interval=interval,
            start_time=start_time,
            extended_trading_hours=extended_trading_hours
        )
        
        # Define an asynchronous generator to listen for candles
        async for event in streamer.listen(Candle):
            # Debug: Print all attributes of the event
            # print(dir(event))  # Uncomment if you need to inspect attributes
            
            # Access the correct attribute for the symbol
            symbol = event.event_symbol  # Updated from event.symbol to event.event_symbol
            if symbol in candles_data:
                candles_data[symbol].append(event)
                logger.info(f"Received candle for {symbol}: {event}")
                
                # Convert event.time to timezone-aware datetime if necessary
                if isinstance(event.time, (int, float)):
                    event_time = datetime.fromtimestamp(event.time / 1000, tz=timezone.utc)
                elif isinstance(event.time, datetime) and event.time.tzinfo is not None:
                    event_time = event.time
                else:
                    # Handle unexpected formats or make assumptions
                    event_time = datetime.fromtimestamp(event.time / 1000, tz=timezone.utc)
                
                if event_time >= end_time:
                    logger.info(f"Reached end_time for {symbol}. Unsubscribing...")
                    await streamer.unsubscribe_candle(
                        symbols=[symbol],
                        interval=interval,
                        start_time=start_time,
                        extended_trading_hours=extended_trading_hours
                    )
                    
                    # Check if all symbols have reached end_time
                    all_done = all(
                        any(
                            (datetime.fromtimestamp(candle.time / 1000, tz=timezone.utc) if isinstance(candle.time, (int, float)) else candle.time) >= end_time
                            for candle in candles_data[sym]
                        )
                        for sym in symbols
                    )
                    if all_done:
                        logger.info("All symbols have reached end_time. Exiting listener loop.")
                        break  # Exit the listening loop
    
    return candles_data

def get_unix_epoch_ms(dt: datetime) -> int:
    """
    Convert a timezone-aware datetime object to Unix epoch time in milliseconds.

    :param dt: Timezone-aware datetime object
    :return: Unix epoch time in milliseconds
    """
    return int(dt.timestamp() * 1000)

async def main():
    # Define the symbols you want to fetch
    symbols = ['AAPL']

    # Define the candle interval
    interval = '5m'  # Options: '15s', '5m', '1h', '3d', '1w', '1mo', etc.

    # Define the time range for historical data using timezone-aware datetime objects
    end_datetime = datetime.now(timezone.utc)
    start_datetime = end_datetime - timedelta(days=7)  # Last 7 days

    # Fetch historical candles
    candles = await fetch_historical_candles(
        symbols=symbols,
        interval=interval,
        start_time=start_datetime,
        end_time=end_datetime,
        extended_trading_hours=False  # Set to True if you want extended hours
    )

    # Example: Print the number of candles fetched for each symbol
    for symbol, data in candles.items():
        logger.info(f"Total candles fetched for {symbol}: {len(data)}")

if __name__ == "__main__":
    asyncio.run(main())



