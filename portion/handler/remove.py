from typing import Annotated

import typer

from portion.base import HandlerBase
from portion.commands import RemoveCommand


class RemoveHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app)

    def register_commands(self) -> None:
        @self.command.command(
            help="Remove a template from the project",
            no_args_is_help=True
        )
        def remove(
            template_name: Annotated[
                str,
                typer.Argument(help="Name of the template to remove")
            ]
        ) -> None:
            RemoveCommand().remove(template_name)
