from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()
client = httpx.AsyncClient()

def get_temporary_directory():
    directory = tempfile.TemporaryDirectory()
    try:
        yield directory.name
    finally:
        del directory

@app.post("/run_jupyter_notebook/{project_id}/{file_name}")
async def run_jupyter_notebook(
    project_id: str,
    file_name: str,
    directory: tempfile.TemporaryDirectory = Depends(get_temporary_directory)
    ) -> Response:

    project = await client.get(f'http://file_server:8000/get_project/{project_id}')
    for file in project.json()['files']:
        with open(Path(str(directory)) / file['name'], 'wb') as f:
            f.write(bytes(file['content'], 'utf-8'))

    temporary_notebook: Path = Path(str(directory)) / file_name

    cmd = ['jupyter', 'nbconvert', '--execute', '--to', 'notebook', str(temporary_notebook), '--output', 'result.ipynb']
    try:
        process = await asyncio.create_subprocess_exec(*cmd)
        await asyncio.wait_for(process.communicate(), timeout=3600)
    except asyncio.TimeoutError:
        process.kill()
        await process.communicate()

    print(f'[NbConvertApp] {process.returncode=}')
    if process.returncode != 0:
        raise HTTPException(status_code=500, detail={
        'status': 'error during notebook execution',
    })

    result_file = Path(str(directory)) / 'result.ipynb'
    result = await client.post(f'http://file_server:8000/add_file/{project_id}', files={
        'file': (result_file.name, result_file.read_bytes()),
    })

    return Response(status_code=200)

