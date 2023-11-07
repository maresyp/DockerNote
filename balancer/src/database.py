from __future__ import annotations

import pymongo


class DatabaseConnection:
    _instance: DatabaseConnection | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, client: str, db_name: str) -> None:
        self.client_name: str = client
        self.db_name: str = db_name

    def __enter__(self):
        self._client = pymongo.MongoClient(self.client_name)
        self.db = self._client.get_database(self.db_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()
