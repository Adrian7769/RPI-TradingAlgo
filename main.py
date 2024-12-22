import time
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from SlackBot.Utils import config
from SlackBot.Source.data import Data
from SlackBot.Source.studies import Studies
from SlackBot.Utils.utils import Utilities
from SlackBot.Source.constant import symbols
from logs.Logging_Config import setup_logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo

# ----------------- Alerts ----------------- #

from SlackBot.Alerts.Conditional.Playbook.pvat import Pvat
from SlackBot.Alerts.Conditional.Contextual.neutral import Neutral
from SlackBot.Alerts.Periodic.ib_check import IB_Check
from SlackBot.Alerts.Periodic.economic import Econ # Econ Will Contain Methods to Store The Days Economic events for #BSND
from SlackBot.Alerts.Periodic.gap_check import Gap_Check
from SlackBot.Alerts.Periodic.lunch import Lunch

# ----------------- Alerts ----------------- #

async def main():
    start_time = time.time()
    
    # Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialization 
    data = Data()
    studies = Studies()
    utils = Utilities()
    
    logger.debug()
    es_bias, nq_bias, rty_bias, cl_bias = utils.grab_bias(config.set_bias)
    config.set_bias(es_bias, nq_bias, rty_bias, cl_bias)
    logger.debug()
    
# --------------- APSCHEDULER --------------- #
# This means that there needs to be a way for Conditional Alerts to be Fed Real time data
# and for periodic alerts, they need to be able to grab the data they need at a moments notice.
# Feed Data, Read Data.
    est = ZoneInfo('America/New_York')
    scheduler = BackgroundScheduler(timezone=est)
    
    # Schedule Econ Alert at 8:45 AM EST every day
    scheduler.add_job(
        Econ.send_alert,
        trigger=CronTrigger(hour=8, minute=45, timezone=est),
        name='Economic Alert'
    )
    # Schedule Gap Check Equity 9:30 AM EST every day
    scheduler.add_job(
        Gap_Check.send_alert,
        trigger=CronTrigger(hour=9, minute=30,second=5, timezone=est),
        name='Gap Check Equity'
    )      
    # Schedule Gap Check Crude at 9:00 AM EST every day
    scheduler.add_job(
        Gap_Check.send_alert,
        trigger=CronTrigger(hour=9, minute=0, second=6, timezone=est),
        name='Gap Check Crude'
    )    
    # Schedule IB Equity Alert at 10:30 AM EST every day
    scheduler.add_job(
        IB_Check.send_alert,
        trigger=CronTrigger(hour=10, minute=30, second=1, timezone=est),
        name='IB Equity Alert'
    )
    # Schedule IB Crude Alert at 10:00 AM EST every day
    scheduler.add_job(
        IB_Check.send_alert,
        trigger=CronTrigger(hour=10, minute=00, second=1, timezone=est),
        name='IB Crude Alert'
    )
    # Schedule Equity Lunch Alert at 12:00 PM EST every day
    scheduler.add_job(
        Lunch.send_alert,
        trigger=CronTrigger(hour=12, minute=00, second=1, timezone=est),
        name='IB Crude Alert'
    )    
    scheduler.start()
    logger.info("APScheduler started.")      
    
    # Main Loop
    async for candle in data.stream_candle_data(symbols, '5min'):
        await data.write_data([candle])
        
        # Feed Relavent Data to Studies
        
        # Feed Relavent Studies to Alerts
        
        # Conditonal Alerts
        
        # Periodic Alerts
        
        symbol = candle['EventSymbol']
        df = await data.read_data(symbol, limit=200)
    
    # Exit Point and Exit Logic
    # Build Auto Exit Logic (No Need for user input)
    # Export Alerts to google sheets
    
if __name__ == "__main__":
    asyncio.run(main())