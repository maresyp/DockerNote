from __future__ import annotations

from typing import Self

from . import server


class Balancer:

    instance: Balancer | None = None

    def __new__(cls) -> Self:
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:

        # TODO(maresyp): make this configurable from .env
        server_names: set[str] = {'nb_worker_1', 'nb_worker_2', 'nb_worker_3'}
        self.servers: list[server.Server] = [
            server.Server(f"http://{server_name}:8000") for server_name in server_names
        ]

    def get_free_server(self) -> server.Server | None:
        for _server in self.servers:
            if not _server.is_locked():
                print(f'INFO: Load Balancer: Requested: {_server} with lock.')
                return _server
        print('WARN: Load Balancer: All servers are busy.')
        return None
