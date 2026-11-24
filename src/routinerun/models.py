from dataclasses import dataclass
from typing import List

@dataclass
class RunnerResult:
    stdout: str
    stderr: str
    returncode: int

@dataclass
class PipelineStep:
    name: str
    command: str

@dataclass
class Pipeline:
    name: str
    description: str
    steps: List[PipelineStep]