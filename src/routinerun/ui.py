from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True)

class UI:
    def error(self, text: str) -> None:
        error_console.print(f'[red][-] {text}[/red]')

    def warning(self, text: str) -> None:
        console.print(f'[yellow][!] {text} [/yellow]')

    def yaml_pipelines_table(self, pipelines: dict) -> None:
        table = Table(title='Pipeline files')

        table.add_column('Path to file')
        table.add_column('Name')
        table.add_column('Description')

        if not pipelines:
            self.warning('Pipelines not found!')
            return
        
        for pipeline in pipelines.values():
            file_path = str(pipeline.source_path) if pipeline.source_path else '-'
            description = pipeline.description or '-'
            table.add_row(file_path, pipeline.name, description)

        console.print(table)