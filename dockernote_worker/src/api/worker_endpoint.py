import subprocess

from fastapi import APIRouter


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
        return {
            'status': 'ok',
            'result': result.stdout.decode('utf-8'),
        }
