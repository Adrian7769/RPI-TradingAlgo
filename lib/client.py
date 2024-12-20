import httpx
import asyncio 
import json
from lib.auth import TastyTradeAuth
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
from typing import (
    Optional, 
    Dict, 
    Any, 
    List
    )
import re
from datetime import datetime

class TastyTradeClient():
    def __init__(self, base_url : str, user_agent: str):
        self.base_url = base_url
        self.user_agent = user_agent
        self.auth = TastyTradeAuth(base_url, user_agent)
        self.client = httpx.AsyncClient() # AHHHHHHHHHHHHHHHHHH
        
        
        