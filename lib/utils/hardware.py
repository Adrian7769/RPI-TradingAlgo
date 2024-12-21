# Contains functions to fectch system data and interact with RPI5 Hardware

from logs.Logging_Config import setup_logging
from gpiozero import TonalBuzzer
from RPLCD.i2c import CharLCD
import os
import logging 
import time

# Setup Logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize LCD
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,        
    port=1,
    cols=16,
    rows=2,
    dotsize=8,
    charmap='A00',
    auto_linebreaks=True
)

# Initialize Buzzer once
buzzer = TonalBuzzer(17) 

def get_cpu_load():
    """Retrieve the current CPU load as a percentage."""
    try:
        load_avg = os.getloadavg()[0]
        cpu_count = os.cpu_count()
        cpu_load = (load_avg / cpu_count) * 100
        return f"CPU Load: {cpu_load:.1f}%"
    except Exception as e:
        logger.error(f"Error getting CPU load: {e}")
        return "CPU Load: N/A"

def get_cpu_temp():
    """Retrieve the current CPU temperature in Celsius."""
    try:
        temp_str = os.popen("vcgencmd measure_temp").readline()
        temp = temp_str.replace("temp=", "").replace("'C\n", "")
        return f"Temp: {temp}C"
    except Exception as e:
        logger.error(f"Error getting CPU temp: {e}")
        return "Temp: N/A"

def display_info():
    """Display CPU load and temperature on the LCD."""
    try:
        lcd.clear()
        load = get_cpu_load()
        temp = get_cpu_temp()
        
        lcd.write_string(load)
        lcd.cursor_pos = (1, 0)  
        lcd.write_string(temp)
        lcd.write_string(
            
        )
    except Exception as e:
        logger.error(f"Failed to activate LCD display: {e}")

def activate_buzzer(frequency=660, duration=1):
    """Activate the buzzer with a specific frequency and duration."""
    try:
        logger.info(f"Activating buzzer with frequency {frequency}Hz for {duration} seconds")
        buzzer.play(frequency)
        time.sleep(duration)
        buzzer.stop()
        logger.info("Buzzer deactivated")
    except Exception as e:
        logger.error(f"Failed to activate buzzer: {e}")

def check_thresholds(cpu_load, cpu_temp):
    """Activate the buzzer if CPU load or temperature exceeds thresholds."""
    HIGH_LOAD_THRESHOLD = 75.0 
    HIGH_TEMP_THRESHOLD = 70.0  
    
    alert = False
    if cpu_load > HIGH_LOAD_THRESHOLD:
        alert = True
    if cpu_temp > HIGH_TEMP_THRESHOLD:
        alert = True
    
    if alert:
        activate_buzzer()

def main():
    """Main loop to update the LCD and check thresholds."""
    try:
        while True:
            display_info()
            # Parse numeric values from display strings
            try:
                load_value = float(get_cpu_load().split(": ")[1].replace("%", ""))
                temp_value = float(get_cpu_temp().split(": ")[1].replace("C", ""))
                activate_buzzer()
                check_thresholds(load_value, temp_value)
            except (IndexError, ValueError) as e:
                logger.error(f"Error parsing CPU metrics: {e}")
            
            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        lcd.clear()
        lcd.close()  # Properly close the LCD connection
        print("Program terminated by user.")

if __name__ == "__main__":
    main()     
    

