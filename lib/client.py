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
        self.client = httpx.AsyncClient() 
        
    async def authenticate(self, username: str, password: Optional[str] = None, remember_token: Optional[str] = None):
        # Create the Current Session
        await self.auth.create_session(username, password, remember_token)
        
    async def destroy_session(self):
        # Destroy the Current Session
        await self.auth.destroy_session()
        
    def get_headers(self) -> Dict[str, str]:
        # Constructs headers for API Requests, including Authorization if available
        headers  = {
            'User-Agent': self.user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.auth.session_token:
            headers['Authorization'] = self.auth.session_token
        return headers
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Makes Async Get Request to the specified endpoint with optional query parameters.
        
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        
        try: 
            response = await self.client.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            raise APIError(f"An Error Occured while Sending Get Request to: {e.request.url!r}.") from e
        
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Make async post request to the specified endpoint with optional query parameters.
        
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        
        try:
            response = await self.client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            raise APIError(f"An Error Occured while sending post request to: {e.request.url!r}") from e
        
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Make async put request to the specified endpoint with optional query parameters.
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers() 
        
        try:
            response = await self.client.put(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            raise APIError(f"An Error Occured While Sending put Request to: {e.request.url!r}") from e
        
    async def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        
        try:
            response = await self.client.delete(url, headers=headers, json=data)
            if response.status_code in [200, 204]:
                if response.status_code == 204:
                    return {}
                return response.json()
            else:
                await self.auth.handle_error(response)
        except httpx.RequestError as e:
            raise APIError(f"An Error occured while sending Delete Request to: {e.request.url!r}") from e
        
            
        
    
        
        
        
        
        
        