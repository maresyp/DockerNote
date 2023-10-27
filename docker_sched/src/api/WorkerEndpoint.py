import uvicorn
import subprocess
from fastapi import FastAPI, APIRouter


class WorkerEndpoint:
    def __init__(self, *args, **kwargs):
        self.router = APIRouter()
        self.router.add_api_route('/run_jupyter_notebook', self.run_jupyter_notebook, methods=['GET'])

    @staticmethod
    def run_jupyter_notebook(notebook):
        cmd = ['jupyter', 'nbconvert', '--execute', '--to', 'notebook', notebook]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=3600)
        if result.returncode != 0:
            return {
                'status': 'error',
            }
        else:
            return {
                'status': 'ok',
                'result': result.stdout.decode('utf-8')
            }


if __name__ == '__main__':
    app = FastAPI()
    worker = WorkerEndpoint()
    app.include_router(worker.router)

    uvicorn.run(app, host='0.0.0.0', port=8000)
