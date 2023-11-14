from __future__ import annotations

from typing import Any

import pymongo


class DatabaseConnection:
    _instance: DatabaseConnection | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.client_name: str = 'client'
        self.db_name: str = 'db_name'

        self._client: pymongo.MongoClient[Any] = pymongo.MongoClient(self.client_name)
        self.db = self._client.get_database(self.db_name)

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()
