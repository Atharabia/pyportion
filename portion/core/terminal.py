from __future__ import annotations

import questionary
from rich.console import Console
from rich.jupyter import JupyterMixin
from rich.prompt import Confirm
from rich.theme import Theme

from portion.models import cli_state


class Terminal:
    def __new__(cls) -> Terminal:
        if not hasattr(cls, "_instance"):
            cls._instance = super(cls, Terminal).__new__(cls)
        return cls._instance

    def __init__(self) -> None:

        theme = Theme({
            "info": "#47ba47",
            "warn": "yellow",
            "error": "red",
        })

        self.console = Console(theme=theme)

    def pulse(self, message: str, **kwargs: str) -> None:
        if cli_state.verbose:
            self.console.log(message.format(**kwargs))

    def info(self, message: str, **kwargs: str) -> None:
        message = message.format(**kwargs)
        self.console.print(f"[info]{message}[/info]")

    def warn(self, message: str, **kwargs: str) -> None:
        message = message.format(**kwargs)
        self.console.print(f"[warn]{message}[/warn]")

    def error(self, message: str, **kwargs: str) -> None:
        message = message.format(**kwargs)
        self.console.print(f"[error]{message}[/error]")

    def prompt(self, message: str, **kwargs: str) -> bool:
        message = message.format(**kwargs)
        if Confirm.ask(message):
            return True
        return False

    def choose(self, message: str, choices: list[str], **kwargs: str) -> str:
        select_style = questionary.Style([
            ("question", "bold #47ba47"),
            ("qmark", "#47ba47"),
            ("pointer", "#47ba47"),
            ("highlighted", "#47ba47"),
            ("answer", "bold #47ba47"),
        ])

        message = message.format(**kwargs)
        choice = questionary.select(message,
                                    choices=choices,
                                    qmark="●",
                                    pointer=">",
                                    style=select_style).ask()
        return choice

    def print(self, message: JupyterMixin) -> None:
        self.console.print(message)
