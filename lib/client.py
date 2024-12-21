# lib/client.py

import httpx
import asyncio 
import json
import logging
from lib.auth import TastyTradeAuth
from lib.utils import retry
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
from logs.Logging_Config import sanitize_payload

logger = logging.getLogger(__name__)

class TastyTradeClient:
    def __init__(self, base_url: str, user_agent: str):
        self.base_url = base_url
        self.user_agent = user_agent
        self.auth = TastyTradeAuth(base_url, user_agent)
        self.client = httpx.AsyncClient()
        logger.debug(f"Initialized TastyTradeClient")

    async def authenticate(self, username: str, password: Optional[str] = None, remember_token: Optional[str] = None):
        logger.info("Starting Authentication Process.")
        await self.auth.create_session(username, password, remember_token)
        logger.info("Authentication Successful.")

    async def destroy_session(self):
        logger.info("Destroying session.")
        await self.auth.destroy_session()
        logger.info("Session destroyed.")

    def get_headers(self) -> Dict[str, str]:
        headers = {
            'User-Agent': self.user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.auth.session_token:
            headers['Authorization'] = self.auth.session_token
            logger.debug("Added Authorization header to request.")
        return headers
    
    @retry(max_attempts=5, backoff_factor=2.0)
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        logger.debug(f"GET Request to {url} with params={params} and headers={sanitize_payload(headers)}")

        try: 
            response = await self.client.get(url, headers=headers, params=params)
            logger.debug(f"Received response: {response.status_code} {response.reason_phrase}")
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Response data: {data}")
                return data
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            logger.error(f"RequestError during GET request to {e.request.url!r}: {e}")
            
    @retry(max_attempts=5, backoff_factor=2.0) 
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        logger.debug(f"POST Request to {url} with data={data} and headers={sanitize_payload(headers)}")

        try:
            response = await self.client.post(url, headers=headers, json=data)
            logger.debug(f"Received response: {response.status_code} {response.reason_phrase}")
            if response.status_code == 200:
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")
                return response_data
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            logger.error(f"RequestError during POST request to {e.request.url!r}: {e}")
            raise APIError(f"An Error Occured while sending post request to: {e.request.url!r}") from e
        
    @retry(max_attempts=5, backoff_factor=2.0)
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        logger.debug(f"PUT Request to {url} with data={data} and headers={sanitize_payload(headers)}")

        try:
            response = await self.client.put(url, headers=headers, json=data)
            logger.debug(f"Received response: {response.status_code} {response.reason_phrase}")
            if response.status_code == 200:
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")
                return response_data
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            logger.error(f"RequestError during PUT request to {e.request.url!r}: {e}")
            raise APIError(f"An Error Occured While Sending put Request to: {e.request.url!r}") from e

    @retry(max_attempts=5, backoff_factor=2.0)
    async def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        logger.debug(f"DELETE Request to {url} with data={data} and headers={sanitize_payload(headers)}")

        try:
            response = await self.client.delete(url, headers=headers, json=data)
            logger.debug(f"Received response: {response.status_code} {response.reason_phrase}")
            if response.status_code in [200, 204]:
                if response.status_code == 204:
                    logger.info("DELETE request successful with no content.")
                    return {}
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")
                return response_data
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            logger.error(f"RequestError during DELETE request to {e.request.url!r}: {e}")
            raise APIError(f"An Error occured while sending Delete Request to: {e.request.url!r}") from e

        
            
        
    
        
        
        
        
        
        