from ..core import Runner
from ..models import RunnerResult

def start_pipeline(name: str) -> RunnerResult:
    return Runner().run(name)