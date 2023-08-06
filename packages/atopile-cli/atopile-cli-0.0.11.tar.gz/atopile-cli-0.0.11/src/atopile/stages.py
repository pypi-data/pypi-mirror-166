import logging
import shlex
from hashlib import sha1
from pathlib import Path
from typing import Dict, List, Optional, Union
import os

import aiodocker
import yaml
from attrs import define

from . import config
from .utils import AtopileError, SubLog, add_file_to_hash, add_obj_to_hash, merge_dict
from .git_resource import GitResource, GitRepoStore, split_path

log = logging.getLogger(__name__)

STAGE_DIR = config.ATOPILE_DIR / 'stages'

@define
class StageDef:
    path: str
    image: str
    command: str
    inputs: Dict[str, Dict[str, str]]
    outputs: Dict[str, Dict[str, str]]

    @classmethod
    def from_file(cls, file: Path):
        with file.open('r') as f:
            stage_raw: dict = yaml.safe_load(f)

        path = stage_raw.get('path')
        image = stage_raw.get('image')
        command = stage_raw.get('command', None)
        inputs = stage_raw.get('inputs', {})
        outputs = stage_raw.get('outputs', {})
        return cls(
            path=path,
            image=image,
            command=command,
            inputs=inputs,
            outputs=outputs,
        )

stage_def_repo_store = GitRepoStore(STAGE_DIR).load()

class StageIO:
    """
    Base class of "things that can be input to stages"
    """
    typename: str

    @property
    def reference(self) -> str:
        raise NotImplementedError

    @property
    def fs_location(self) -> Path:
        raise NotImplementedError

    @classmethod
    def check(cls, candidate: str):
        raise NotImplementedError

    @classmethod
    def from_data(cls, candidate_data, def_data: dict, project_dir: Path):
        if not def_data.get('list', False):
            candidates = [candidate_data]
        else:
            candidates = candidate_data

        for candidate in candidates:
            for T in (Handle, File):
                if T.check(candidate):
                    return T.from_string(candidate, def_data, project_dir)

@define
class File(StageIO):
    """
    Represents a file in the filesystem from the start of compile time
    """
    path: Path

    @property
    def reference(self) -> str:
        return str(self.path)

    @property
    def fs_location(self) -> Path:
        return self.path

    @classmethod
    def check(cls, candidate: str):
        return True

    @classmethod
    def from_string(cls, candidate: str, def_data: dict, project_dir: Path):
        full_path = project_dir / candidate
        return cls(
            path=full_path, 
        )

@define
class Handle(StageIO):
    """
    Represents a direct output of another stage having been run
    """
    stage: str
    output_name: str
    typename: str
    filename: str
    glob_pattern: str
    project_dir: Path

    _SPLITTING_CHAR = ':'

    @property
    def reference(self) -> str:
        return f'{self.stage}:{self.output_name}'

    @property
    def fs_location(self) -> Union[Path, List[Path]]:
        if self.filename:
            return self.project_dir / 'build' / self.stage / self.filename
        if self.glob_pattern:
            return (self.project_dir / 'build' / self.stage).glob(self.glob_pattern)

    def exists(self):
        if self.filename:
            return self.fs_location.exists()
        if self.glob_pattern:
            return len(list(self.fs_location))

    @classmethod
    def check(cls, candidate: str):
        return cls._SPLITTING_CHAR in candidate

    @classmethod
    def from_stage_name_def_data(cls, stage_name: str, output_name: str, def_data: dict, project_dir: Path):
        glob_pattern = def_data.get('pattern')
        filename = def_data.get('filename')
        if not (glob_pattern or filename):
            raise ValueError('No glob pattern of filename specified for output')

        return cls(
            stage=stage_name, 
            output_name=output_name, 
            typename=def_data['type'],
            filename=filename,
            glob_pattern=glob_pattern,
            project_dir=project_dir,
        )

    @classmethod
    def from_string(cls, candidate: str, def_data: dict, project_dir: Path):
        stage_name, output_name = candidate.split(cls._SPLITTING_CHAR)
        return cls.from_stage_name_def_data(stage_name, output_name, def_data, project_dir)
        
@define
class Stage:
    name: str
    stage_def: StageDef
    dist: Dict[str, str]
    inputs: Dict[str, StageIO]
    outputs: Dict[str, Handle]
    project_dir: Path
    after: List[str]

    def compute_hash(self) -> Optional[str]:
        hash = sha1()
        add_obj_to_hash(self, hash)
        for input in self.inputs.values():
            if not input.fs_location.exists():
                # can't compute the hash if all the inputs aren't available
                return
            else:
                add_file_to_hash(input.fs_location, hash)
        return hash.hexdigest()

    async def run(self, docker: aiodocker.Docker, inputs: Dict[str, Union[StageIO, List[StageIO]]]) -> SubLog:
        stage_log = SubLog(self.name)
        prj = self.project_dir
        build = self.project_dir / 'build' / self.name

        # build commands
        # reference for config structure: https://docs.docker.com/engine/api/v1.41/#tag/Container/operation/ContainerList
        docker_config = merge_dict(
            {
                'Image': self.stage_def.image,
                'HostConfig': {
                    'Binds': [
                        f'{str(prj)}:/prj:ro',
                        f'{str(build)}:/build:rw'
                    ]
                }
            },
            config.options.get('docker_options', {})
        )

        # do input substitutions
        cmd = self.stage_def.command
        for input in inputs:
            var_name = f'${input}'
            if var_name in cmd:
                var_inputs = inputs[input]
                if not isinstance(var_inputs, list):
                    var_inputs = [var_inputs]

                # rehome them for use in the container
                rerooted_inputs = []
                prj = Path('/prj')
                for i in var_inputs:
                    path = str(i.fs_location).replace(str(self.project_dir), str(prj))
                    rerooted_inputs += [str(path)]
                var_value = ','.join(rerooted_inputs)

                cmd = cmd.replace(var_name, var_value)

        if cmd:
            docker_config['Cmd'] = shlex.split(cmd)

        log.debug(f'docker commands: {docker_config}')
        docker_cli_bind_mounts = [f'-v {b}' for b in docker_config.get('HostConfig', {}).get('Binds', [])]
        docker_cli_str = f'docker run --rm -it {" ".join(docker_cli_bind_mounts)} {docker_config.get("Image")} {" ".join(docker_config.get("Cmd", []))}'
        log.debug(f'docker cli equiv: "{docker_cli_str}"')
        container: aiodocker.docker.DockerContainer = await docker.containers.create_or_replace(
            config=docker_config,
            name=self.name,
        )
        try:
            await container.start()
            exit_data = await container.wait()
            stdout = await container.log(stdout=True) #, follow=True)
            stderr = await container.log(stderr=True) #, follow=True)
        finally:
            await container.stop(force=True)
            await container.delete(force=True)

        exit_status = exit_data['StatusCode']
        if exit_status:
            stage_log.error(f'Stage exited with code {exit_status}')
        else:
            stage_log.info(f'Stage complete with code {exit_status}')

        for stdout_line in stdout:
            stage_log.info(stdout_line)

        for stderr_line in stderr:
            stage_log.info(stderr_line)

        return stage_log

    @classmethod
    def ios_from_stage_def(cls, log, logger, name: str, stage_def: StageDef, data: dict, project_dir: Path):
        # build io dicts
        inputs = {}
        for input_name, input_def_data in stage_def.inputs.items():
            if input_name in data:
                input_config_data = data[input_name]
            elif 'default' in input_def_data:
                input_config_data = input_def_data['default']
            else:
                log.error(f'No input data for {input_name}')

            try:
                inputs[input_name] = StageIO.from_data(input_config_data, input_def_data, project_dir)
            except (ValueError, KeyError) as ex:
                logger.error(f'{repr(ex)} raised while processing {input_name}')

        outputs = {}
        for output_name, output_def_data in stage_def.outputs.items():
            try:
                outputs[output_name] = Handle.from_stage_name_def_data(name, output_name, output_def_data, project_dir)
            except (ValueError, KeyError) as ex:
                logger.error(f'{repr(ex)} raised while processing {output_name}')

        # bail out here, we can't return a valid object
        if not log:
            log.show()
            raise AtopileError

        return inputs, outputs

    @classmethod
    def from_dict(cls, name: str, data: dict, project_dir: Path):
        log = SubLog(name, logging.DEBUG)
        logger = log.logger

        # common stuff
        dist = data.get('dist') or {}  # None -> empty dict as well
        if isinstance(dist, list):
            dist = {k: None for k in dist}
        elif isinstance(dist, str):
            dist = {dist: None}

        after = data.get('after')
        if not after:
            after = []
        elif isinstance(after, str):
            after = [after]

        # stage defining
        stage_def_path = data.get('path')
        image = data.get('image')

        # make sure image and path are mutally exclusive
        if not stage_def_path and not image:
            log.error('No image or path provided for this stage to run')
            raise AtopileError
        if stage_def_path and image:
            log.error('Both an image and path provided for this stage')
            raise AtopileError

        # complex stages
        if stage_def_path:
            stage_def_remote, stage_def_internal = split_path(stage_def_path)
            stage_def_resource: GitResource = stage_def_repo_store.load().get(stage_def_remote)
            stage_def: StageDef = StageDef.from_file(stage_def_resource.local / stage_def_internal)
            if not stage_def:
                logger.error(f'StageDef with path "{stage_def_path}" not found')
                log.show()
                raise ValueError

            inputs, outputs = cls.ios_from_stage_def(log, logger, name, stage_def, data, project_dir)

        # "simple" stages
        if image:
            command = data.get('command')
            if not command:
                log.error(f'No command provided for {name}')
                raise AtopileError

            stage_def = StageDef(
                None,
                image,
                command,
                inputs={},
                outputs={},
            )

            inputs = {}
            outputs = {}
        
        # build the final class
        return cls(
            name=name,
            stage_def=stage_def,
            dist=dist,
            inputs=inputs,
            outputs=outputs,
            project_dir=project_dir,
            after=after,
        )

    @classmethod
    def from_config_data(cls, task_data: dict, project_dir: Path):
        stage_configs = {}
        for name, task_data in task_data.items():
            stage_configs[name] = cls.from_dict(name, task_data, project_dir)
        return stage_configs

    @classmethod
    def from_config_path(cls, project_dir: Path):
        config_path = project_dir / '.atopile.yaml'
        with config_path.open('r') as f:
            config_data = yaml.safe_load(f)
        return cls.from_config_data(config_data, project_dir)
