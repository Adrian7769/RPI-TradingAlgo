# data_fetch.py
# data_fetch.py will be responsible for fetching data from external sources.
import asyncio
import os 
import logging
from logs.Logging_Config import setup_logging
from dotenv import load_dotenv
import sqlalchemy
from tastytrade import Session, DXLinkStreamer

class Data():
    def __init__(self):
        pass
    async def fetch_candle_data(self, symbol, period, start_date, end_date, data_type):
        # Fetch Data from API Source and return it in a structured manner for write data to store it into a database. Needs to be able to handle Real time and historical data.
        pass
    async def fetch_option_data(self, symbol, period, start_date, end_date, data_type):
        # Fetch Option data from api source and return it in a structured manner for write data to store it into a database. Needs to be able to handle Real time and historical data.
        pass
    async def write_data(self, data, data_type):
        # Needs to be able to store data from historical data sources and real time data sources into a databse
        pass
    async def read_data(self, data_type):
        # This is primarly for the Indicators in the tools directory to get fed real time data in a structured manner so that we can run conditional statements on them as they update in real time.
        # The indicators will be constantly accessing the database in real time as it is updating so that I can run calculations
        # on the data as it is updating in real time.
        pass

