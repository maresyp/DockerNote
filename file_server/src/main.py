from __future__ import annotations

from typing import Any

import pymongo
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

from .models.project import Project, ProjectCollection

app = FastAPI()
client: pymongo.MongoClient[Any] = pymongo.MongoClient('db-files')
db = client.get_database('projects')
projects_collection = db.get_collection('projects')

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
    return Response(status_code=201)

@app.get(
    "/list_projects/{owner_id}",
    response_description="Get projects names corresponding to the given owner_id",
    )
async def list_projects(owner_id: str) -> dict[str, str]:
    projects = list(projects_collection.find({'owner_id': owner_id}))
    return {
        project['_id']: project['title']  for project in projects
    }
