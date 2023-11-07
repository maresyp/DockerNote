from __future__ import annotations

import shutil
import subprocess

from fastapi import APIRouter, File, UploadFile


class WorkerEndpoint:
    def __init__(self, *args, **kwargs):
        self.router = APIRouter()
        self.router.add_api_route('/run_jupyter_notebook', self.run_jupyter_notebook, methods=['POST'])

    @staticmethod
    def run_jupyter_notebook(notebook: UploadFile = File(...)): # noqa: B008
        try:
            with open(notebook.filename, 'wb') as f:
                shutil.copyfileobj(notebook.file, f)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            notebook.file.close()

        cmd = ['jupyter', 'nbconvert', '--execute', '--to', 'notebook', notebook.filename]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=3600)
        if result.returncode != 0:
            return {
                'status': 'error',
                'file': notebook.filename,
            }
        return {
            'status': 'ok',
            'file': notebook.filename,
            'result': result.stdout.decode('utf-8'),
        }
