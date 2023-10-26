import luigi
import subprocess
from pathlib import Path

class RunJupyterNotebook(luigi.Task):
    notebook: Path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.notebook.replace('.ipynb', 'html'))

    def run(self):
        cmd: str = ['jupyter', 'nbconvert', '--execute', '--to', 'notebook', self.notebook]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=3600)


if __name__ == '__main__':
    luigi.build([RunJupyterNotebook(notebook='test.ipynb')], local_scheduler=True)