from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse


class WorkerEndpoint:
    def __init__(self, *args, **kwargs):
        self.router = APIRouter()
        self.router.add_api_route('/run_jupyter_notebook', self.run_jupyter_notebook, methods=['POST'])

    @staticmethod
    def run_jupyter_notebook(notebook: UploadFile = File(...)) -> FileResponse: # noqa: B008
        with tempfile.TemporaryDirectory() as tmpdirname:
            temporary_notebook: Path = Path(tmpdirname) / notebook.filename
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
