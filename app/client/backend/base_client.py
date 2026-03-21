"""Shared HTTP client for all backend modules.

A single httpx.AsyncClient is instantiated for the whole application,
enabling connection-pool reuse.
"""

import httpx

from app.core.config import settings

http_client = httpx.AsyncClient(base_url=settings.BACKEND_URL, timeout=10.0)
