from gpiozero import Buzzer
from RPLCD.i2c import CharLCD
import os
import logging 
import time
from typing import Optional
from decimal import Decimal
from datetime import datetime, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import gspread

logger = logging.getLogger(__name__)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(r"SlackBot\Utils\Credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Methods To Do Various Things
class Utilities():
    def __init__(self):
        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=0x27,        
            port=1,
            cols=16,
            rows=2,
            dotsize=8,
            charmap='A00',
            auto_linebreaks=True
        )
        self.buzzer = Buzzer(17)
    def cpu_load(self) -> str:
        try:
            load_avg = os.getloadavg()[0]
            cpu_count = os.cpu_count()
            cpu_load = (load_avg / cpu_count) * 100
            return f"CPU Load: {cpu_load:.1f}%"
        except Exception as e:
            logger.error(f"Error getting CPU load: {e}")
            return "CPU Load: N/A"
    def cpu_temp(self) -> str:
        try:
            temp_str = os.popen("vcgencmd measure_temp").readline()
            temp = temp_str.replace("temp=", "").replace("'C\n", "")
            return f"Temp: {temp}C"
        except Exception as e:
            logger.error(f"Error getting CPU temp: {e}")
            return "Temp: N/A"
    def display_activate(self) -> Optional[str]:
        try:
            self.lcd.clear()
            load = self.cpu_load()
            temp = self.cpu_temp()
            self.lcd.write_string(load)
            self.lcd.cursor_pos = (1, 0)  
            self.lcd.write_string(temp)
            self.lcd.write_string()
        except Exception as e:
            logger.error(f"Error displaying info: {e}")
            return "Error displaying info"
    def buzzer_activate(self, duration: Optional[Decimal] = None) -> None:
        try:
            self.buzzer.on()
            time.sleep(Decimal(duration))
            self.buzzer.off()
        except Exception as e:
            logger.error(f"Error activating buzzer: {e}")
            return "Error activating buzzer"
        pass
    def _to_datetime(self, raw_time):
        if isinstance(raw_time, (int, float)):
            return datetime.fromtimestamp(raw_time / 1000, tz=timezone.utc)
        return raw_time    
    def grab_bias(self, set_bias):
        logger.debug(f" Startup | grab_impvol | Note: Running")
        
        output_bias = {}

        for task in set_bias:
            workbook = client.open_by_key(task["sheet_id"])
            sheet = workbook.worksheet(task["sheet_name"])
            cell_value = sheet.cell(task["row_number"], task["col_number"]).value
            
            logger.debug(f" Startup | grab_bias | Sheet: {task['sheet_name']} | Row: {task['row_number']}  | Column: {task['col_number']}")
            
            if "ES" in task["sheet_name"]:
                output_bias['es_bias'] = cell_value
            elif "NQ" in task["sheet_name"]:
                output_bias['nq_bias'] = cell_value
            elif "RTY" in task["sheet_name"]:
                output_bias['rty_bias'] = cell_value
            elif "CL" in task["sheet_name"]:
                output_bias['cl_bias'] = cell_value
                
        es_bias = output_bias['es_bias']
        nq_bias = output_bias['nq_bias']
        rty_bias = output_bias['rty_bias']
        cl_bias = output_bias['cl_bias']
 
        logger.debug(f" Startup | grab_bias | ES_Bias: {es_bias} | NQ_Bias: {nq_bias} | RTY_Bias: {rty_bias} | CL_Bias: {cl_bias}")
        return es_bias, nq_bias, rty_bias, cl_bias        
    def timzone_update(self):
        # Will Contain Code to Scrape The TimeZone Values from Investing.com and Update the Existing Investpy Library
        pass
        
        
            
    
        
        
        
        