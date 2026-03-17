from typing import Annotated

import typer

from portion.base import HandlerBase
from portion.commands import NewCommand


class NewHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app)

    def register_commands(self) -> None:
        @self.command.command(
            help="Create a new project from a template",
            no_args_is_help=True
        )
        def new(
                template_name: Annotated[
                    str,
                    typer.Argument(help="Name of the template")
                ],
                project_name: Annotated[
                    str,
                    typer.Argument(help="Name of the new project")
                ]) -> None:
            NewCommand().new(template_name, project_name)
