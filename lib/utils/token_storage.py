# Contains Utils For Managing Return Tokens

import os 
import json
import logging

logger = logging.getLogger(__name__)

TOKENS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../tokens.json')

def save_token(remember_token: str):
    try:
        with open(TOKENS_FILE, 'w') as f:
            json.dump({'remember_token': remember_token}, f)
        logger.info("Remember token saved successfully")
    except Exception as e:
        logger.error(f"Failed to Save remember token: {e}")
def load_token() -> str:
    try:
        with open(TOKENS_FILE, 'r') as f:
            data = json.load(f)
            remember_token = data.get('remember_token')
            logger.debug("Remember Token Loaded Successfully")
            return remember_token
    except FileNotFoundError:
        logger.error("Tokens File Not Found")
        return None
    except Exception as e:
        logger.error(f"Failed to Load Remember Token: {e}")
        return None
    