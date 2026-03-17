from typing import Annotated

import typer

from portion.base import HandlerBase
from portion.commands import TemplateCommand


class TemplateHandler(HandlerBase):
    def __init__(self, app: typer.Typer) -> None:
        super().__init__(app, "template")

    def register_commands(self) -> None:
        @self.command.command(
            name="download",
            help="Download templates by link or project config",
        )
        def download(
            link: Annotated[
                str | None,
                typer.Argument(
                    help="Link to the template to download"
                )
            ] = None,
            version: Annotated[
                str | None,
                typer.Argument(
                    help="Template version. e.g v1.0.0"
                )
            ] = None,
        ) -> None:
            TemplateCommand().download(link, version)

        @self.command.command(
            name="remove",
            help="Remove a template",
            no_args_is_help=True
        )
        def remove(
            template_name: Annotated[
                str,
                typer.Argument(help="Name of the template to remove")
            ]
        ) -> None:
            TemplateCommand().remove(template_name)

        @self.command.command(
            name="list",
            help="List all available templates"
        )
        def list() -> None:
            TemplateCommand().list()

        @self.command.command(
            name="info",
            help="Display information about a template",
            no_args_is_help=True
        )
        def info(
            template_name: Annotated[
                str,
                typer.Argument(help="Name of the template")
            ]
        ) -> None:
            TemplateCommand().info(template_name)
