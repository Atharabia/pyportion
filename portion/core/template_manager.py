from __future__ import annotations

import os
import shutil

from git import Repo
from platformdirs import user_data_dir
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from ruamel.yaml import YAML

from portion.models import Config
from portion.models import TemplateConfig


class TemplateManager:
    def __new__(cls) -> TemplateManager:
        if not hasattr(cls, "_instance"):
            cls._instance = super(cls, TemplateManager).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._pyportion_path = os.path.join(user_data_dir(),
                                            Config.portion_dir)

    def create_pyportion_dir(self) -> None:
        if not os.path.exists(self._pyportion_path):
            os.mkdir(self._pyportion_path)

    def is_template_exists(self, template_name: str) -> bool:
        template_path = os.path.join(self._pyportion_path, template_name)
        return os.path.exists(template_path)

    def download_template(self, link: str) -> bool:
        template_name = link.split("/")[-1]
        template_path = os.path.join(self._pyportion_path, template_name)
        try:
            Repo.clone_from(link, template_path)
            return True
        except Exception:
            return False

    def delete_if_not_template(self, template_name: str) -> bool:
        template_path = os.path.join(self._pyportion_path, template_name)
        portion_json_path = os.path.join(template_path,
                                         Config.portion_file)
        if not os.path.exists(portion_json_path):
            shutil.rmtree(template_path)
            return True
        return False

    def delete_template(self, template_name: str) -> bool:
        template_path = os.path.join(self._pyportion_path,
                                     template_name)

        if os.path.exists(template_path):
            shutil.rmtree(template_path)
            return True
        return False

    def get_templates(self) -> list[str]:
        return os.listdir(self._pyportion_path)

    def copy_template(self, template_name: str, project_name: str) -> None:
        template_path = os.path.join(self._pyportion_path,
                                     template_name,
                                     "base")

        shutil.copytree(src=template_path,
                        dst=project_name,
                        dirs_exist_ok=True)

    def copy_portion(self,
                     template_name: str,
                     portion_path: list[str],
                     dest_path: list[str]) -> None:

        path = os.path.join(self._pyportion_path,
                            template_name,
                            ".portions",
                            *portion_path)

        dest = os.path.join(*dest_path)
        shutil.copyfile(path, dest)

    def read_configuration(self, template_name: str) -> TemplateConfig:
        path = os.path.join(self._pyportion_path,
                            template_name,
                            Config.portion_file)

        yaml = YAML()
        with open(path, "r") as f:
            data = yaml.load(f)
        return TemplateConfig(**data)

    def update_configuration(self,
                             template_name: str,
                             config: TemplateConfig) -> None:
        path = os.path.join(self._pyportion_path,
                            template_name,
                            Config.portion_file)

        yaml = YAML()
        with open(path, "w") as f:
            yaml.dump(config.model_dump(), f)

    def get_template_info(self, template_config: TemplateConfig) -> Panel:
        config = template_config.model_dump()

        metadata = {k: v for k, v in config.items() if isinstance(v, str)}
        portions = config.get("portions", []) or []

        def build_table(data) -> Table | None:
            if not data:
                return None

            table = Table(show_header=False,
                          box=None,
                          title_style="cyan bold",
                          expand=False)

            for key, value in data.items():
                table.add_row(
                    f"[bold cyan]{key.capitalize()}[/]",
                    str(value),
                )
            return table

        metadata_table = build_table(metadata)

        portions_table = None
        if portions:

            portions_table = Table(
                "[bold cyan]Portions:[/]",
                show_header=True,
                box=None,
                expand=False)

            for i, portion in enumerate(portions):
                portion_name = portion.get("name", str(portion))
                portions_table.add_row(f"{i + 1}. {portion_name}")

        group_items = [
            table for table
            in (metadata_table, portions_table)
            if table
        ]

        group = Group(*group_items)
        return Panel(
            group,
            title="[bold cyan]Template Info[/]",
            border_style="cyan",
            expand=False
        )
