from typing import Annotated

import typer

from portion.base import HandlerBase
from portion.commands import AddCommand


class AddHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app)

    def register_commands(self) -> None:
        @self.command.command(
            help="Add a template to the project",
            no_args_is_help=True
        )
        def add(
            template_name: Annotated[
                str,
                typer.Argument(help="Name of the template to add")
            ]
        ) -> None:
            AddCommand().add(template_name)
