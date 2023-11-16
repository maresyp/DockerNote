from pathlib import Path

import aiofiles
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from . import balancer
from . import server

app = FastAPI()
load_balancer: balancer.Balancer = balancer.Balancer()

@app.get("/")
async def read_root():
    server: server.Server = load_balancer.get_server()
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
        return None


async def run_notebook(self, worker_name: str) -> None:
    nb_path = Path('app/my_notebook.ipynb')
    async with aiofiles.open(nb_path, 'rb') as f:
        file = {'notebook': ('my_notebook.ipynb', await f.read(), 'application/octet-stream')}
        response = await self.client.post(worker_name, files=file, timeout=3600)
        # extract file from response and save it
        with open('got.ipynb', 'wb') as file:
            file.write(response.content)
        print(f'{response.content=}')