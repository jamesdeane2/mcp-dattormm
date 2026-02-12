"""HTTP client for Datto RMM API with OAuth 2.0 authentication."""

import asyncio
import base64
from datetime import datetime, timedelta

import httpx

from .config import get_settings


class DattoRMMError(Exception):
    """Base exception for Datto RMM API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class DattoRMMAuthError(DattoRMMError):
    """Authentication failed (401/403)."""
    pass


class DattoRMMNotFoundError(DattoRMMError):
    """Resource not found (404)."""
    pass


class DattoRMMValidationError(DattoRMMError):
    """Invalid request parameters (400/422)."""
    pass


class DattoRMMRateLimitError(DattoRMMError):
    """Rate limited (429)."""

    def __init__(self, message: str, retry_after: int | None = None):
        super().__init__(message, 429)
        self.retry_after = retry_after


class DattoRMMServerError(DattoRMMError):
    """Server-side failure (5xx)."""
    pass


class DattoRMMClient:
    """Async HTTP client for Datto RMM API."""

    RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
    BASE_RETRY_DELAY = 1.0
    MAX_RETRY_DELAY = 60.0

    def __init__(self):
        self.settings = get_settings()
        self._client: httpx.AsyncClient | None = None
        self._access_token: str | None = None
        self._token_expires: datetime | None = None

    async def _ensure_token(self) -> str:
        """Get valid access token, refreshing if needed."""
        if self._access_token and self._token_expires and datetime.now() < self._token_expires:
            return self._access_token

        # Request new token
        auth = base64.b64encode(b"public-client:public").decode()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.auth_url,
                headers={
                    "Authorization": f"Basic {auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "password",
                    "username": self.settings.api_key,
                    "password": self.settings.api_secret
                },
                timeout=self.settings.timeout
            )
            if response.status_code == 401:
                raise DattoRMMAuthError("Invalid API credentials", 401)
            if response.status_code == 403:
                raise DattoRMMAuthError("Access forbidden", 403)
            if response.status_code != 200:
                raise DattoRMMAuthError(f"Authentication failed: {response.text}", response.status_code)

            data = response.json()
            self._access_token = data["access_token"]
            # Token valid for 100 hours, refresh at 90 hours to be safe
            self._token_expires = datetime.now() + timedelta(hours=90)
            return self._access_token

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.settings.api_url,
                timeout=self.settings.timeout
            )
        return self._client

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make authenticated request with retry logic."""
        token = await self._ensure_token()
        client = await self._get_client()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"

        for attempt in range(self.settings.max_retries):
            response = await client.request(method, path, headers=headers, **kwargs)

            if response.status_code == 401:
                # Token expired, clear and retry
                self._access_token = None
                self._token_expires = None
                token = await self._ensure_token()
                headers["Authorization"] = f"Bearer {token}"
                continue

            if response.status_code == 404:
                raise DattoRMMNotFoundError(f"Resource not found: {path}", 404)

            if response.status_code in (400, 422):
                raise DattoRMMValidationError(f"Validation error: {response.text}", response.status_code)

            if response.status_code == 403:
                raise DattoRMMAuthError(f"Access forbidden: {response.text}", 403)

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    delay = int(retry_after)
                else:
                    delay = min(self.BASE_RETRY_DELAY * (2 ** attempt), self.MAX_RETRY_DELAY)
                await asyncio.sleep(delay)
                continue

            if response.status_code in self.RETRYABLE_STATUSES:
                delay = min(self.BASE_RETRY_DELAY * (2 ** attempt), self.MAX_RETRY_DELAY)
                await asyncio.sleep(delay)
                continue

            if response.status_code >= 500:
                raise DattoRMMServerError(f"Server error: {response.text}", response.status_code)

            if response.status_code >= 400:
                raise DattoRMMError(f"API error {response.status_code}: {response.text}", response.status_code)

            # Handle empty responses (some endpoints return no body)
            if response.status_code == 204 or not response.content:
                return {"success": True}

            return response.json()

        raise DattoRMMError("Max retries exceeded")

    async def get(self, path: str, **kwargs) -> dict:
        """HTTP GET request."""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> dict:
        """HTTP POST request."""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> dict:
        """HTTP PUT request."""
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> dict:
        """HTTP DELETE request."""
        return await self._request("DELETE", path, **kwargs)

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


_client: DattoRMMClient | None = None


def get_client() -> DattoRMMClient:
    """Get or create client singleton."""
    global _client
    if _client is None:
        _client = DattoRMMClient()
    return _client


def reset_client() -> None:
    """Reset client for testing."""
    global _client
    _client = None
