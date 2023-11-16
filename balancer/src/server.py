import asyncio

import httpx


class Server:
    def __init__(self, url: str) -> None:
        self.url = url
        self._lock = asyncio.Lock()
        self.client = httpx.AsyncClient()

    def __str__(self) -> str:
        return f'{self.url}'

    async def __aenter__(self):
        await self._lock.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()

    def is_locked(self) -> bool:
        return self._lock.locked()
