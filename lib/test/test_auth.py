import os
import asyncio
import logging
from dotenv import load_dotenv
from logs.Logging_Config import setup_logging
from lib.client import TastyTradeClient
from lib.exceptions import (
    APIError,
    UnauthorizedError,
    NotFoundError,
    TooManyRequestsError,
    BadRequestError,
    ForbiddenError,
    UnprocessableContentError,
    ServerError,    
)
load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("TASTY_BASE")
USER_AGENT = os.getenv("TASTY_AGENT")
USERNAME = os.getenv("TASTY_USER")
PASSWORD = os.getenv("TASTY_PASS")

async def main():
    client = TastyTradeClient(base_url=BASE_URL, user_agent=USER_AGENT)
    try:
        logger.info("Authentication with Tasty Trade Beginnning")
        await client.authenticate(username=USERNAME, password=PASSWORD)
        logger.info("Authenticatioin with Tasty Trade API Successful")
        
        logger.info("Testing and Fetching account information...")
        account_info = await client.get("/customers/me")
        logger.info(f"Account information: {account_info}")
    except (APIError, UnauthorizedError, NotFoundError, TooManyRequestsError,
            BadRequestError, ForbiddenError, UnprocessableContentError, ServerError) as e:
        logger.error(f"API Error Occcured: {e}")
    except Exception as e:
        logger.error(f"An Unknown Error has occured: {e}")
    finally:
        logger.info("Destroying Session...")
        await client.destroy_session()
        logger.info("Session destroyed")
if __name__ == "__main__":
    asyncio.run(main())
        
        


