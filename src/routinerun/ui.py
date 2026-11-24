from rich.console import Console

error_console = Console(stderr=True)

class UI:
    def error(self, text: str) -> None:
        error_console.print(f'[red][-] {text}[/red]')