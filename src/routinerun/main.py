import typer

from .tools import get_yaml_pipeline, start_pipeline
from .ui import UI

app = typer.Typer(help='Utility for managing team pipelines', add_completion=False)

@app.command('list')
def list_pipeline():
    """Command to view all pipelines"""
    get_yaml_pipeline()

@app.command('start')
def start(name: str = typer.Argument(..., help='Name pipeline')):
    """Command for start pipeline file"""
    result = start_pipeline(name)
    ui = UI()

    if result.stdout:
        typer.echo(result.stdout)

    if result.stderr:
        typer.echo(result.stderr, err=True)

    if result.returncode != 0:
        ui.warning(f'Pipeline "{name}" completed with code {result.returncode}')
        raise typer.Exit(code=result.returncode)


if __name__ == '__main__':
    app()