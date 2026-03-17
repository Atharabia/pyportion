from typing import Annotated

import typer

from portion.base import HandlerBase
from portion.commands import InitCommand


class InitHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app)

    def register_commands(self) -> None:
        @self.command.command(
            help="Make current project a PyPortion project",
            no_args_is_help=True
        )
        def init(
            project_name: Annotated[
                str,
                typer.Argument(help="Name of the project")
            ]
        ) -> None:
            InitCommand().init(project_name)
