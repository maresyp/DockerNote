from __future__ import annotations

import asyncio
from typing import Any, Self


class Balancer:

    instance: Balancer | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, amount_of_workers: int, worker_names: set[str]) -> None:

        if amount_of_workers != len(worker_names):
            raise ValueError('Amount of workers and worker names are not equal')

        self.load: asyncio.Queue[Any] = asyncio.Queue(amount_of_workers)
        self.workers: list[asyncio.Task[None]] = [
                asyncio.create_task(self.get_worker(worker_names.pop())) for _ in range(amount_of_workers)
            ]

    async def get_worker(self, worker_name: str) -> None:
        worker_url: str = f'http://{worker_name}:8000/run_jupyter_notebook'
        while True:
            try:
                load = await self.load.get()
                async with load['client'] as client:
                    response = await client.post(worker_url, files=load['files'], timeout=3600)
                    print(f'{response.content=}')
            finally:
                self.load.task_done()
