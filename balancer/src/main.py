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
        response = await client.post("http://worker:8312/run_jupyter_notebook", files=file)
        print(f'{response=}')