from ..core import YAMLParser
from ..ui import UI

def get_yaml_pipeline() -> None:
    pipelines = YAMLParser()._load_all()

    UI().yaml_pipelines_table(pipelines)