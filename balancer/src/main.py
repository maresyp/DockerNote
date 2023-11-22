from pathlib import Path

import aiofiles
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response

from . import balancer, server

app = FastAPI()
load_balancer: balancer.Balancer = balancer.Balancer()

@app.get("/")
async def read_root():
    _server: server.Server = load_balancer.get_server()
    nb_path = Path('app/my_notebook.ipynb')
    url: str = _server.url + '/run_jupyter_notebook'
    async with aiofiles.open(nb_path, 'rb') as f:
        file = {'notebook': ('my_notebook.ipynb', await f.read(), 'application/octet-stream')}
        response = await _server.client.post(url, files=file, timeout=3600)
        # extract file from response and save it
        with open('got.ipynb', 'wb') as file:
            file.write(response.content)
        print(f'{response.content=}')
    return {"Hello": "World"}

@app.post("/run_jupyter_notebook")
async def run_jupyter_notebook(notebook: UploadFile = File(...)) -> FileResponse:
    server: server.Server | None = load_balancer.get_free_server()
    if server is None:
        raise HTTPException(status_code=503, detail={
            'status': 'all servers busy',
            'file': notebook.filename,
        })

    async with server:
        url: str = server.url + '/run_jupyter_notebook'
        response = await server.client.post(url, files={'notebook': notebook.file}, timeout=3600)
        print(f'{response.content=}')
        with open('got.ipynb', 'wb') as file:
            file.write(response.content)
        return None

@app.post("/add_project")
async def add_project(
    id: str,
    owner_id: str,
) -> Response:
    _server: server.Server = load_balancer.get_server()
    async with _server:
        url: str = _server.url + '/add_project'
        body = {
            'id': id,
            'owner_id': owner_id,
        }
        print(f"INFO: Balancer: sending to : {url}")
        response = await _server.client.post(url, json=body)
        return Response(status_code=response.status_code)
