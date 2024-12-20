# lib/auth.py

import httpx
import asyncio
import json
import logging
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
from datetime import datetime, timedelta
from typing import Optional
from logs.Logging_Config import sanitize_payload

logger = logging.getLogger(__name__)

class TastyTradeAuth:
    def __init__(self, base_url: str, user_agent: str):
        self.base_url = base_url
        self.user_agent = user_agent
        self.session_token: Optional[str] = None
        self.remember_token: Optional[str] = None
        self.session_expiration: Optional[datetime] = None
        self.client = httpx.AsyncClient()
        logger.debug(f"Initialized TastyTradeAuth")

    async def create_session(self, username: str, password: Optional[str] = None, remember_token: Optional[str] = None):
        logger.info("Attempting to create a new session.")
        url = f"{self.base_url}/sessions"
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {"login": username, "remember-me": True}

        # Ensure parameters are provided
        if password:
            payload["password"] = password
            logger.debug("Using password for authentication.")
        elif remember_token:
            payload["remember-token"] = remember_token
            logger.debug("Using remember token for authentication.")
        else:
            logger.error("Neither password nor remember token provided.")
            raise ValueError("Either password or remember token must be provided")

        logger.debug(f"POST {url} with payload: {sanitize_payload(payload)}")

        try:
            response = await self.client.post(url, headers=headers, json=payload)
            logger.debug(f"Received response: {response.status_code} {response.reason_phrase}")
            if response.status_code in [200, 201]:
                data = response.json().get("data", {})
                logger.debug(f"Session data received: {sanitize_payload(data)}")
                self.session_token = data.get("session-token")
                self.remember_token = data.get("remember-token")
                expiration_str = data.get("session-expiration")
                if expiration_str:
                    self.session_expiration = datetime.fromisoformat(expiration_str.rstrip("Z"))
                    logger.info(f"Session will expire at {self.session_expiration}")
                else:
                    logger.warning("Session expiration not provided in the response.")
                logger.info("Session created successfully.")
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                await self.handle_error(response)
        except httpx.RequestError as e:
            logger.error(f"RequestError while creating session: {e}")
            raise APIError(f"An Error Occurred while requesting {e.request.url!r}") from e

    async def destroy_session(self):
        logger.info("Attempting to destroy the current session.")
        if not self.session_token:
            logger.warning("No active session to destroy.")
            return

        url = f"{self.base_url}/sessions"
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": self.session_token,
            "Content-Type": "application/json"
        }

        logger.debug(f"DELETE {url} with headers: {headers}")

        try:
            response = await self.client.delete(url, headers=headers)
            logger.debug(f"Received response: {response.status_code} {response.reason_phrase}")
            if response.status_code == 204:
                logger.info("Session destroyed successfully.")
                self.session_token = None
                self.remember_token = None
                self.session_expiration = None
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                await self.handle_error(response)
        except httpx.RequestError as e:
            logger.error(f"RequestError while destroying session: {e}")
            raise APIError(f"An error occurred while requesting {e.request.url!r}") from e

    async def handle_error(self, response: httpx.Response):
        try:
            error = response.json().get("error", {})
            code = error.get("code", "Unknown Error")
            message = error.get("message", "No message provided")
            
            # Log the entire response for debugging
            logger.error(f"API responded with error: {response.status_code} {code} - {message}")
            logger.debug(f"Response content: {response.text}")

            # Handle API Exceptions by raising the appropriate exception
            match response.status_code:
                case 400:
                    raise BadRequestError(f"Bad Request: {code} - {message}")
                case 401:
                    self.session_token = None
                    raise UnauthorizedError(f"Unauthorized: {code} - {message}")
                case 403:
                    raise ForbiddenError(f"Forbidden: {code} - {message}")
                case 404:
                    raise NotFoundError(f"Not Found: {code} - {message}")
                case 422:
                    raise UnprocessableContentError(f"Unprocessable Content: {code} - {message}")
                case 429:
                    raise TooManyRequestsError(f"Too Many Requests: {code} - {message}")
                case 500:
                    raise ServerError(f"Server Error {response.status_code}: {code} - {message}")
                case _:
                    raise APIError(f"Unexpected Error {code} - {message}")
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from response: {response.text}")
            response.raise_for_status()

                
            
        
                
        
        
        
        
        


