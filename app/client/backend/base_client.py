"""Client HTTP partagé entre tous les modules backend.

Un seul httpx.AsyncClient est instancié pour toute l'application,
ce qui permet la réutilisation du pool de connexions.
"""

import httpx

from app.core.config import settings

http_client = httpx.AsyncClient(base_url=settings.BACKEND_URL, timeout=10.0)
