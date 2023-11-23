from __future__ import annotations

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import Response

from . import balancer, server

app = FastAPI()
load_balancer: balancer.Balancer = balancer.Balancer()

async def run_jupyter_notebook(server: server.Server, url: str) -> None:
    async with server:
        await server.client.post(url, timeout=3600)

@app.get("/run_file/{project_id}/{file_name}")
async def run_file(background_tasks: BackgroundTasks, project_id: str, file_name: str) -> Response:
    server: server.Server | None = load_balancer.get_free_server()
    if server is None:
        raise HTTPException(status_code=503, detail={
            'status': 'all servers busy',
        })

    url: str = server.url + f'/run_jupyter_notebook/{project_id}/{file_name}'
    background_tasks.add_task(run_jupyter_notebook, server, url)
    return Response(status_code=200)
