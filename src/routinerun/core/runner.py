import subprocess

from typing import List

from .parser import YAMLParser
from ..models import RunnerResult, PipelineStep

class Runner:
    def __init__(self):
        self.yaml_parser = YAMLParser()

    def run(self, pipeline_name: str) -> RunnerResult:
        pipeline = self.yaml_parser.get_pipeline(pipeline_name)

        stdout_parts: List[str] = []
        stderr_parts: List[str] = []
        last_returncode = 0

        for step in pipeline.steps:
            res = self._run_step(step)
            last_returncode = res.returncode

            if res.stdout:
                stdout_parts.append(f'[{step.name}]\n{res.stdout.rstrip()}')
            if res.stderr:
                stderr_parts.append(f'[{step.name}]\n{res.stderr.rstrip()}')

            if res.returncode != 0:
                break

        return RunnerResult(
            stdout="\n".join(stdout_parts),
            stderr="\n".join(stderr_parts),
            returncode=last_returncode,
        )

    def _run_step(self, step: PipelineStep) -> RunnerResult:
        try:
            result = subprocess.run(
                step.command,
                text=True,
                capture_output=True
            )
            return RunnerResult(
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
            )
        except FileNotFoundError as exc:
            return RunnerResult(
                stdout='',
                stderr=f'Command is not found ({step.command[0]}): {exc}',
                returncode=127,
            )