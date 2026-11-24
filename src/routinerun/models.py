from dataclasses import dataclass
from typing import List
from pathlib import Path

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
    source_path: Path | None = None