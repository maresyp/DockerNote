from fastapi import FastAPI

from .api.worker_endpoint import WorkerEndpoint

app = FastAPI()
worker = WorkerEndpoint()
app.include_router(worker.router)

