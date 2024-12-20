import httpx
import asyncio
import json
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

class TastyTradeAuth:
    def __init__(self, base_url: str, user_agent : str):
        self.base_url = base_url
        self.user_agent = user_agent
        self.session_token: Optional[str] = None
        self.remember_token: Optional[str] = None
        self.session_expiration: Optional[datetime] = None
        self.client = httpx.AsyncClient()
        
    async def create_session(self, username: str, password: Optional[str] = None, remember_token: Optional[str] = None):
        # Define Headers and API ENDPOINT to create a new session
        url = f"{self.base_url}/sessions"
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {"login": username, "remember-me": True}
       
        # Make Sure Params are Provided 
        if password:
            payload["password"] = password
        elif remember_token:
            payload["remember-token"] = remember_token
        else:
            raise ValueError("Either password or remember token must be provided")
        
        # Make Post Request to API End Point to Open Up a New Session 
        try:
            response = await self.client.post(url, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                data = response.json().get("data", {})
                self.session_token = data.get("session-token")
                self.remember_token = data.get("remember-token")
                expiration_str =  data.get("session-expiration")
                self.session_expiration = datetime.fromisoformat(expiration_str.rstrip("Z"))
            else: 
                await self.handle_error(response)
        except httpx.RequestError as e:
            raise APIError(f"An Error Occured while requesting {e.request.url!r}") from e
        
    async def destroy_session(self):
        if not self.session_token:
            print("No Active Session To Destroy")
            return
        
        url = f"{self.base_url}/sessions"
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": self.session_token,
            "Content-Type": "application/json"
        }
        
        try:
            response = await self.client.delete(url, headers=headers)
            if response.status_code == 204:
                print("Session Destroyed Successfully")
                self.session_token = None
                self.remember_token = None
                self.session_expiration = None
            else:
                await self.handle_error(response)
        except httpx.RequestError as e:
            raise APIError(f"An error occured while requesting {e.request.url!r}") from e
        
    async def handle_error(self, response: httpx.Response):
        
        try:
            error = response.json().get("error", {})
            code = error.get("code", "Unknown Error")
            message = error.get("message", "No message provided")
            
            # Handles API Exceptions by raising the right excpetion Handler
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
                    raise UnprocessableContentError(f"Unproccessable Content: {code} - {message}")
                case 429:
                    raise TooManyRequestsError(f"Too Many Requests: {code} - {message}")
                case 500:
                    raise ServerError(f"Server Error {response.status_code}: {code} - {message}")
                case _:
                    raise APIError(f"Unexpected Error {code} - {message}")
        except json.JSONDecodeError:
            response.raise_for_status()
                
            
        
                
        
        
        
        
        


