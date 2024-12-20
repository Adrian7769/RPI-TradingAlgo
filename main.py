from openai import OpenAI
from dotenv import load_dotenv
import os 
import base64
from pathlib import Path
from logs.Logging_Config import setup_logging
import logging
import subprocess
import time
from datetime import timedelta
from lib import auth
load_dotenv()

# Logging setup
setup_logging()
logger = logging.getLogger(__name__)

def audio(file_path):
    try:
        subprocess.run(['mpg123', str(file_path)], check=True)
        logger.debug(f"Playing audio file: {file_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error Playing Audio file: {e}")
    except FileNotFoundError:
        logger.error(f"mpg123 is not installed or not found in PATH")
def main():
    logger.debug(" Main | Note: Running")
    
    # Fetching Token
    token = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=token)
    speech_file_path = Path(__file__).parent / "test.mp3"
    try:
        # Starting API Response Timer
        api_start = time.time()
        
        # Making API Requests for TTS 
        with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="alloy",
            input="#IBGP Setup Is in Play for Nasdaq Criteria is 5 Out of 10."
        ) as response:
            response.stream_to_file(speech_file_path)
            
        # Logging API Response Time
        api_end = time.time()
        elapsed_time = timedelta(seconds = api_start - api_end)
        logger.info(f"API Response time: {elapsed_time}")
        
        # Checking if File Path Exists
        if speech_file_path.exists():
            
            # Calling audio function
            audio(speech_file_path)
        
    except Exception as e:
        logger.debug(f"An Error occured while creating speech: {e}") 
    return
if __name__ == '__main__':
    main()


