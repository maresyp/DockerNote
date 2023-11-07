from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

def get_temporary_directory():
    directory = tempfile.TemporaryDirectory()
    try:
        yield directory.name
    finally:
        del directory

@app.post("/run_jupyter_notebook")
def run_jupyter_notebook(
    notebook: UploadFile = File(...),
    directory: tempfile.TemporaryDirectory = Depends(get_temporary_directory)
    ) -> FileResponse:

    temporary_notebook: Path = Path(directory) / notebook.filename
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
    result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=3600)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail={
        'status': 'error',
        'file': notebook.filename,
    })

    return FileResponse(temporary_notebook)
