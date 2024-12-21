# Contains Retry Logic for Interacting with API's

import asyncio
import logging
from functools import wraps
from lib.exceptions import TooManyRequestsError, ServerError

logger = logging.getLogger(__name__)

def retry(max_attempts=3, backoff_factor=1.0, allowed_exceptions=(TooManyRequestsError, ServerError)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = backoff_factor
            for attempt in range(1, max_attempts + 1): 
                try:
                    return await func(*args, **kwargs)
                except allowed_exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"Max retry attempts reached for {func.__name__}.")
                        raise
                    logger.warning(f"{e}. Retrying in {delay} seconds.")
                    await asyncio.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator
                    