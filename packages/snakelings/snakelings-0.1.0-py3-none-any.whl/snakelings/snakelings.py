"""CLI interface for snakelings."""
# standard library
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import List
from zipfile import ZipFile

# third-party
import appdirs
import click
from click_default_group import DefaultGroup
import pydantic
import requests
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from snakelings.exercise import Exercise

# first-party


class SnakelingsFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, callback) -> None:
        super().__init__()
        self.callback = callback

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            self.callback(event)


def _download_project_files() -> bytes:
    response = requests.get('https://github.com/cblades/snakelings/archive/refs/heads/project_files.zip', timeout=60)
    if not response.ok:
        print(f'Error downloading project files:\n\n\t{response.status_code} - {response.text}')
        sys.exit(1)
    return response.content

def _gen_default_config():
    return {
        'snakelings_version': '0.1.0',
        'project_version': None,
        'project_directory': None,
    }

def _get_config_file_path() -> Path:
    """Return path to the config file, creating necessary directory structure as needed."""
    config_file_dir_path = Path(appdirs.user_config_dir(appname='charmer', appauthor='cblades'))
    os.makedirs(config_file_dir_path, exist_ok=True)
    return config_file_dir_path/'config.json'

@click.group(cls=DefaultGroup, default='install', default_if_no_args=True)
def cli():
    """Main group."""
    pass

@cli.command()
@click.option('--delete', is_flag=True, show_default=True, default=False, help='Delete configuration (you probably do not want to do this')
def config(delete: bool):
    """Print configuration."""
    config_file_path = _get_config_file_path()

    if delete:
        if config_file_path.exists():
            config_file_path.unlink()

    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        print(config_file.read())

@cli.command()
@click.option('--dirname', default='snakelings', help='Name of the directory containing snakelings project files.')
@click.option('--force', is_flag=True, show_default=True, default=False, help='Force installation even if snakelings is already installed.')
def install(dirname: str, force: bool):
    """Simple program that greets NAME for a total of COUNT times."""
    # TODO check for existing installation
    # TODO handle force flag
    config_file_path = _get_config_file_path()
    project_zip: bytes = _download_project_files()
    with ZipFile(BytesIO(project_zip)) as zip_file:
        zip_file.extractall()
    
    os.rename('snakelings-project_files', dirname)

    config_file_path.touch()
    project_files_path = Path(os.curdir)/dirname
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        with open(project_files_path/'meta.json', encoding='utf-8') as project_meta_file:
            project_meta = json.load(project_meta_file)  # TODO handle failure here
            config_file.write(json.dumps({
                'snakelingsVersion': '0.1.0',  # TODO make this dynamic
                'projectVersion': project_meta.get('projectVersion'),
                'projectPath': str(project_files_path.absolute()),
            }, indent=2))


@cli.command()
def watch():
    """Continuously watch files and guide through exercises."""
    config_file_path = _get_config_file_path()

    if not config_file_path.exists():
        print(
            'Snakelings has not been initialized.\n\n\t'
            'Run `snakelings` in directory you would like to initialize project in.')
        sys.exit(1)

    config = None
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        try:
            config = json.load(config_file)
            if not Path(os.curdir).samefile(Path(config.get('projectPath'))):
                print(f'Run `snakelings watch` from the project directory at:\n\n\t{config.get("projectPath")}')
                sys.exit(1)
        except json.JSONDecodeError:
            print(f'Configuration file at...\n\n\t{config_file_path}\n'
                f'\n...is invalid and can not be read.  Delete file to re-generate.')
            sys.exit(1)
    os.environ['PYTHONDONTWRITEBYTECODE']='1'

    with open(Path(os.curdir)/'meta.json', encoding='utf-8') as meta_file:
        meta = json.load(meta_file)
        # pylint: disable=no-member
        exercises = pydantic.parse_obj_as(List[Exercise], meta.get('exercises'))  
                
        console = Console()
        console.clear()
        with Live(console=console, refresh_per_second=4, transient=True) as live:
            try:
                for i, exercise in enumerate(exercises):
                    progress = int((i/len(exercises)) * 100)
                    done = _is_exercise_done(exercise)
                    if done:
                        continue
                    dirty = False
                    def _callback(event: FileModifiedEvent):
                        nonlocal dirty
                        nonlocal exercise

                        if Path(event.src_path).samefile(exercise.path):
                            dirty = True

                    event_handler = SnakelingsFileSystemEventHandler(_callback)
                    observer = Observer()
                    observer.schedule(event_handler, Path(os.curdir), recursive=True)
                    observer.start()
                    live.update(_run_exercise(exercise, progress))
                    while not done:
                        if dirty:
                            done = _is_exercise_done(exercise)
                            live.update(_run_exercise(exercise, progress))
                            dirty = False
                        time.sleep(0.4)
                    observer.stop()
                    observer.join()
            except KeyboardInterrupt:
                pass

def _format_success_message(output):
    return f'[bold green]{output}[/bold green]\n\n:tada:Congratulations!:tada: If you are done with this exercise, remove the first line of the file: [bold yellow]# I\'M NOT DONE YET[/bold yellow]'


def _format_failure_message(output):
    return Syntax(output, 'Python Traceback')



def _run_exercise(exercise: Exercise, progress) -> Panel:
    cmd = [exercise.executable, exercise.path] 

    if exercise.executable == 'pylint':
        cmd = [exercise.executable, *exercise.pytest_args, exercise.path]

    result = subprocess.run(cmd, capture_output=True, check=False)
    output = f'{result.stdout.decode("utf-8")}{result.stderr.decode("utf-8")}'
    if result.returncode == 0:
        title = f':snake: [bold green]{exercise.path}[/bold green] :snake:'
        message = _format_success_message(output)
    else:
        title = f':red_circle: [bold red]{exercise.path}[/bold red] :red_circle:'
        message = _format_failure_message(output)

    return Panel(
        message,
        title=title,
        subtitle=f'You have finished {progress}% of the exercises!'
    )

def _is_exercise_done(exercise: Exercise) -> bool:
    with open(exercise.path, encoding='utf-8') as f:
        return not f.readline().startswith("# I'M NOT DONE YET")

if __name__ == '__main__':
    watch()
