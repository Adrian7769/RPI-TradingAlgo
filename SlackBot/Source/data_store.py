from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://data_ingestor:Adrianj7769!@localhost:5432/rpi_algo')

def store_candles_to_db(data):
    pass