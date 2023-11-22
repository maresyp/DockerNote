from __future__ import annotations

from typing import Any

import pymongo
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

from .models.project import Project, ProjectCollection, UpdateProject

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
    "/get_project/{project_id}",
    response_description="Get a single project",
)
async def get_project(project_id: str) -> Project:
    project = projects_collection.find_one({'_id': project_id})
    if project is None:
        raise HTTPException(status_code=404, detail={
            'status': 'error: project with this id does not exist',
        })
    return project

@app.put(
    "/update_project/{project_id}",
    response_description="Update a project",
)
async def update_project(project_id: str, project: UpdateProject) -> Response:
    result = projects_collection.find_one_and_update(
        {'_id': project_id},
        {'$set': project.model_dump(by_alias=True)},
    )
    if result is None:
        raise HTTPException(status_code=404, detail={
            'status': 'error: project with this id does not exist',
        })
    return Response(status_code=200)

@app.delete(
    "/delete_project/{project_id}",
    response_description="Delete a project",
)
async def delete_project(project_id: str) -> Response:
    result = projects_collection.delete_one({'_id': project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail={
            'status': 'error: project with this id does not exist',
        })
    return Response(status_code=200)

@app.get(
    "/list_projects/{owner_id}",
    response_description="Get projects names corresponding to the given owner_id",
)
async def list_projects(owner_id: str) -> dict[str, str]:
    projects = list(projects_collection.find({'owner_id': owner_id}))
    return {
        project['_id']: project['title']  for project in projects
    }

@app.post(
    "/add_file/{project_id}",
    response_description="Add a new file to a project",
)
async def add_file(project_id: str, file: UploadFile = File(...)) -> Response:
    project = projects_collection.find_one({'_id': project_id})
    if project is None:
        raise HTTPException(status_code=404, detail={
            'status': 'error: project with this id does not exist',
        })

    try:
        file_content = file.file.read().decode('utf-8')
    except Exception as err:
        raise HTTPException(status_code=500, detail={
            'status': 'error: cannot read file',
        }) from err
    finally:
        file.file.close()

    project['files'].append({
        'name': file.filename,
        'content': file_content,
    })

    result = projects_collection.find_one_and_update(
        {'_id': project_id},
        {'$set': project},
    )
    if result is None:
        raise HTTPException(status_code=404, detail={
            'status': 'error: project with this id does not exist',
        })
    return Response(status_code=200)
