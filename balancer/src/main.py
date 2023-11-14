from pathlib import Path

import aiofiles
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    await run_notebook()
    return {"Hello": "World"}

async def run_notebook():
    client = httpx.AsyncClient()
    nb_path = Path('app/my_notebook.ipynb')
    async with aiofiles.open(nb_path, 'rb') as f:
        file = {'notebook': ('my_notebook.ipynb', await f.read(), 'application/octet-stream')}
        response = await client.post("http://nb_worker_1:8000/run_jupyter_notebook", files=file, timeout=3600)
        # extract file from response and save it
        with open('got.ipynb', 'wb') as file:
            file.write(response.content)
        print(f'{response.content=}')