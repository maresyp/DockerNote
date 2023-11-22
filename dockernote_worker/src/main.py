from __future__ import annotations

import asyncio
import shutil
import tempfile
from pathlib import Path
from typing import Any

import pymongo
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

from .models.project import Project

app = FastAPI()
client: pymongo.MongoClient[Any] = pymongo.MongoClient('db-balancer')
db = client.get_database('projects')
projects_collection = db.get_collection('projects')

def get_temporary_directory():
    directory = tempfile.TemporaryDirectory()
    try:
        yield directory.name
    finally:
        del directory

@app.post("/run_jupyter_notebook")
async def run_jupyter_notebook(
    notebook: UploadFile = File(...),
    directory: tempfile.TemporaryDirectory = Depends(get_temporary_directory)
    ) -> FileResponse:

    await notebook.read()
    await notebook.seek(0)

    print(f"{notebook.file=}")
    if notebook.filename is None:
        raise HTTPException(status_code=400, detail={
            'status': 'error',
            'file': 'no file',
        })

    temporary_notebook: Path = Path(str(directory)) / notebook.filename

    try:
        with Path.open(temporary_notebook, 'wb') as f:
            shutil.copyfileobj(notebook.file, f)
    except OSError as err:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'file': notebook.filename,
        }) from err
    finally:
        notebook.file.close()

    cmd = ['jupyter', 'nbconvert', '--inplace', '--execute', '--to', 'notebook', str(temporary_notebook)]
    try:
        process = await asyncio.create_subprocess_exec(*cmd)
        await asyncio.wait_for(process.communicate(), timeout=3600)
    except asyncio.TimeoutError:
        process.kill()
        await process.communicate()

    print(f'[NbConvertApp] {process.returncode=}')
    if process.returncode != 0:
        raise HTTPException(status_code=500, detail={
        'status': 'error',
        'file': notebook.filename,
    })

    return FileResponse(temporary_notebook)

@app.post(
    "/add_project",
    response_description="Add a new project",
    )
async def add_project(project: Project) -> Response:
    try:
        projects_collection.insert_one(
            project.model_dump(by_alias=True),
        )
    except pymongo.errors.DuplicateKeyError as err:
        raise HTTPException(status_code=409, detail={
            'status': 'error: project with this id already exists',
        }) from err
    print('INFO: created new project')
    return Response(status_code=201)
