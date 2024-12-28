# data.py
# data.py will be responsible for handling data from the API source and then storing it into a database for studies to be build on.
import asyncio
import os 
import logging
from logs.Logging_Config import setup_logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from tastytrade import Session, DXLinkStreamer
from tastytrade.dxfeed import Candle
import pandas as pd
from SlackBot.Utils.utils import Utils

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

USERNAME = os.getenv("TASTY_USER")
PASSWORD = os.getenv("TASTY_PASS")

# SqlAlchemy Engine
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# Data FLow Class to handle all data related operations
class Data():
    def __init__(self):
        self.session = Session(login=USERNAME, password=PASSWORD) # TastyWorks Session
        self.utils = Utils() # Utility Functions
        pass
    
    # Method to fetch data from API Source and return it in a Structured Manner
    async def fetch_candle_data(self, symbol, interval, start_time, end_time, extended_hours=True):
        candles_list = []
        async with DXLinkStreamer(self.session) as streamer:
            await streamer.subscribe_candle(
                symbols=[symbol],
                interval=interval,
                start_time=start_time,
                extended_trading_hours=extended_hours
            )
            async for event in streamer.listen(Candle):
                if event.event_symbol == symbol:
                    continue
                event_dt = self.utils._to_datetime(event.time)
                if event_dt > end_time:
                    await streamer.unsubscribe_candle(
                        symbols=[symbol],
                        interval=interval,
                        start_time=start_time,
                        extended_trading_hours=extended_hours
                    )
                    break
                
                # Structured Data
                candles_list.append({
                    "EventSymbol": event.event_symbol,
                    "EventTime": event_dt,
                    "Index": event.index,
                    "Sequence": event.sequence,
                    "Count": event.count,
                    "Volume": event.volume,
                    "VWAP": event.vwap,
                    "BidVolume": event.bid_volume,
                    "AskVolume": event.ask_volume,
                    "ImpVolatility": event.imp_volatility,
                    "OpenInterest": event.open_interest,
                    "Open": event.open,
                    "High": event.high,
                    "Low": event.low,
                    "Close": event.close
                })
        return candles_list
    
    async def fetch_option_data(self, symbol, period, start_date, end_date, data_type):
        # Need to impliment this later (I REALLLLLLLY DONT WANT TO TO THIIIISSS)
        # Fetch Option data from api source and return it in a structured manner for write data to store it into a database. Needs to be able to handle Real time and historical data.
        pass
    
    # Method to Stream Candle Data from API Source and return it in a structured manner.
    async def stream_candle_data(self, symbol, period, start_date, end_date, data_type):
        async with DXLinkStreamer(self.session) as streamer:
            await streamer.subscribe_candle(
                symbols=[symbol],
                interval=period,
            )
            async for event in streamer.listen(Candle):
                if event.event_symbol == symbol:
                    yield {
                        "EventSymbol": event.event_symbol,
                        "EventTime": self.utils._to_datetime(event.time),
                        "Index": event.index,
                        "Sequence": event.sequence,
                        "Count": event.count,
                        "Volume": event.volume,
                        "VWAP": event.vwap,
                        "BidVolume": event.bid_volume,
                        "AskVolume": event.ask_volume,
                        "ImpVolatility": event.imp_volatility,
                        "OpenInterest": event.open_interest,
                        "Open": event.open,
                        "High": event.high,
                        "Low": event.low,
                        "Close": event.close
                    }       
               
    # Writes Historical and Real Time Candle Data to Database
    async def write_data(self, data, data_type):
        df = pd.DataFrame(data) # Convert Data to DataFrame
        df.to_sql(name="candle_data",engine=engine, if_exists='append', index=False)
        
    # Reads the most 'limit' rows of data for a symbol from the Database
    async def read_data(self, symbol, limit):
        query = f"""
            SELECT * FROM candle_data
            WHERE "EventSymbol" = '{symbol}'
            ORDER BY "EventTime" DESC
            LIMIT {limit};
        """
        df = pd.read_sql(query, engine)
        return df.sort_values("EventTime")