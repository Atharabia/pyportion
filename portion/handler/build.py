from typing import Annotated

import typer

from portion.base import HandlerBase
from portion.commands import BuildCommand


class BuildHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app)

    def register_commands(self) -> None:
        @self.command.command(
            help="Build a new portion in the project",
            no_args_is_help=True
        )
        def build(
            portion_name: Annotated[
                str,
                typer.Argument(help="Name of the portion to build")
            ]
        ) -> None:
            BuildCommand().build(portion_name)
