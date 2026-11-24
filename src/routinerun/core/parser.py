import yaml
import pathlib

from typing import List, Dict

from ..ui import UI
from ..models import Pipeline, PipelineStep

class YAMLParser:
    def __init__(self):
        self.home_dir = pathlib.Path('~/.routinerun').expanduser()
        self.home_dir.mkdir(parents=True, exist_ok=True)

        self.ui = UI()

    def get_pipeline(self, name: str) -> Pipeline:
        pipelines = self._load_all()

        if name not in pipelines:
            available = ", ".join(pipelines.keys()) or 'no pipelines available'
            self.ui.error(f'Pipeline "{name}" not found ({available})')
        return pipelines[name]

    def _parse_single_file(self, file_path: pathlib.Path) -> Pipeline:
        with file_path.open('r', encoding='utf-8') as file:
            raw = yaml.safe_load(file)

            if not isinstance(raw, dict):
                self.ui.error(f'A dictionary was expected at the root {file_path}, get: {type(raw).__name__}')
                return

            steps: List[PipelineStep] = []

            for index, step in enumerate(raw.get('steps')):
                if not isinstance(step, dict):
                    self.ui.error(f'Step #{index + 1} in {file_path} must be a dictionary')
                    return
                
                raw_command = step.get('command')
                if not isinstance(raw_command, list):
                    self.ui.error(f'The "command" field in step #{index + 1} ({file_path}) must be a non-empty list')
                    return 
                
                command = [str(token) for token in raw_command]

                steps.append(
                    PipelineStep(
                        name=step.get('name'),
                        command=command
                    )
                )

            return Pipeline(
                name=raw.get('name'),
                description=str(raw.get('description')),
                steps=steps,
                source_path=file_path
            )
        
    def _load_all(self) -> Dict[str, Pipeline]:
        pipelines: Dict[str, Pipeline] = {}
        files = sorted(
            [*self.home_dir.glob('*.yaml'), *self.home_dir.glob('*.yml')]
        )

        for file_path in files:
            pipeline = self._parse_single_file(file_path)
            pipelines[pipeline.name] = pipeline

        return pipelines    

