import yaml
import pathlib

from dataclasses import dataclass
from typing import List, Dict

from rich.console import Console

@dataclass
class Step:
    name: str
    command: str

@dataclass
class Pipeline:
    name: str
    description: str
    steps: List[Step]

class YAMLParser:
    def __init__(self):
        self.home_dir = pathlib.Path('~/.routinerun').expanduser()
        self.home_dir.mkdir(parents=True, exist_ok=True)

        self.console = Console()

    def get_pipeline(self, name: str) -> Pipeline:
        pipelines = self._load_all()

        if name not in pipelines:
            available = ", ".join(pipelines.keys()) or "no pipelines available"
            self.console.print(f'[red][-] Pipeline "{name}" not found ({available})[/red]')
        return pipelines[name]

    def _parse_single_file(self, file_path: pathlib.Path) -> Pipeline:
        with file_path.open('r', encoding='utf-8') as file:
            raw = yaml.safe_load(file)

            if not isinstance(raw, dict):
                self.console(f'[red][-] A dictionary was expected at the root {file_path}, get: {type(raw).__name__}[/red]')
                return

            steps: List[Step] = []

            for index, step in enumerate(raw.get('steps')):
                if not isinstance(step, dict):
                    self.console.print(f'[red][-] Step #{index + 1} in {file_path} must be a dictionary[/red]')
                    return
                
                raw_command = step.get('command')
                if not isinstance(raw_command, list):
                    self.console.print(f'[red][-] The "command" field in step #{index + 1} ({file_path}) must be a non-empty list[/red]')
                    return 
                
                command = [str(token) for token in raw_command]

                steps.append(
                    Step(
                        name=step.get('name'),
                        command=command
                    )
                )

            return Pipeline(
                name=raw.get('name'),
                description=str(raw.get('description')),
                steps=steps
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

