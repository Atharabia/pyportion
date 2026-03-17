import typer

from portion.base import HandlerBase
from portion.commands import InfoCommand


class InfoHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app)

    def register_commands(self) -> None:
        @self.command.command(
            help="Display project information"
        )
        def info() -> None:
            InfoCommand().info()
