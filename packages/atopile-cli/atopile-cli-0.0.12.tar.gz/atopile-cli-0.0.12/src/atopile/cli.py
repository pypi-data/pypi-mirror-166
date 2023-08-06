import json
import logging
from pathlib import Path

import click

from . import build, stages, config
from .lib import add_lib
from .utils import AtopileError, get_project_dir

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def ensure_dir(dir: Path):
    if not dir.exists():
        dir.mkdir(parents=True)
        log.info(f'creating {str(dir)}')

@click.group()
def cli():
    pass

@cli.command('run')
@click.option(
    '--docker-options', 
    help="""A JSON representation of docker configuration to be sent when spooling up new containers.
        See https://docs.docker.com/engine/api/v1.41/#tag/Container/operation/ContainerList for options""", 
    default=None, 
    type=str
)
@click.argument('task')
@click.argument('project-dir', required=False)
# @click.option('--target', required=False)
def cli_build(docker_options, task, project_dir):
    """Build your project."""
    if project_dir:
        project_dir = Path(project_dir)
    else:
        project_dir = get_project_dir()

    
    if docker_options is not None:
        docker_options = json.loads(docker_options)
        config.options['docker_options'] = docker_options

    try:
        build.build(task, project_dir)
    except AtopileError:
        exit(1)
    
@cli.group('lib')
def lib():
    pass

@lib.command('add')
@click.argument('repo')
@click.option('--project-dir', default=None, help='project to add the dependency to, else project of CWD')
@click.option('--subproject', default='*', help='subproject to add the dependency to, else it\'s added to all. Glob matches .kicad_pro files')
def cli_add_lib(repo, project_dir, subproject):
    """Add a new library to the project's dependencies."""
    if project_dir:
        project_dir = Path(project_dir)
    else:
        project_dir = get_project_dir()

    add_lib(repo, subproject, project_dir)
    
@cli.group('stage-def')
def stage_def():
    pass

@stage_def.command('add')
@click.argument('path', required=False)
def cli_stage_def_add(path):
    """Add a search path to stages."""
    if not path:
        path = Path('.')
    if Path(path).exists() and not Path(path).is_dir():
        path = Path(path).parent
    stages.stage_def_repo_store.add(str(path))

@stage_def.command('replace')
@click.argument('path', required=False)
def cli_stage_def_replace(path):
    """Add a search path to stages."""
    if not path:
        path = Path('.')
    if Path(path).exists() and not Path(path).is_dir():
        path = Path(path).parent
    stages.stage_def_repo_store.replace(str(path))

@stage_def.command('scan-local')
def cli_stage_def_scan_local():
    """Add a search path to stages."""
    stages.stage_def_repo_store.scan_local()

@stage_def.command('update')
def cli_stage_def_scan_local():
    """Add a search path to stages."""
    for entry in stages.stage_def_repo_store.entries:
        entry.update()

if __name__ == '__main__':
    cli()
