import sys
from contextlib import contextmanager

from rich.console import Console as RichConsole

console = RichConsole()
_err_console = RichConsole(stderr=True)


def success(message: str) -> None:
    console.print(f"[green]✓[/] {message}")


def error(message: str) -> None:
    _err_console.print(f"[bold red]✗[/] {message}")


def warn(message: str) -> None:
    console.print(f"[yellow]![/] {message}")


def info(message: str) -> None:
    console.print(f"[blue]ℹ[/] {message}")


@contextmanager
def status(message: str):
    with console.status(message):
        yield
