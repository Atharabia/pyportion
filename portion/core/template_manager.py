from __future__ import annotations

import os
import shutil
import tempfile

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
        os.makedirs(self._pyportion_path, exist_ok=True)

    def _version_path(self, template_name: str, version: str) -> str:
        version = version.lstrip("v")
        return os.path.join(self._pyportion_path, template_name, version)

    def is_template_exists(self, template_name: str) -> bool:
        path = os.path.join(self._pyportion_path, template_name)
        return os.path.exists(path) and bool(os.listdir(path))

    def is_version_exists(self, template_name: str, version: str) -> bool:
        return os.path.exists(self._version_path(template_name, version))

    def get_template_versions(self, template_name: str) -> list[str]:
        path = os.path.join(self._pyportion_path, template_name)
        if not os.path.exists(path):
            return []
        return ["v" + d for d in os.listdir(path) if not d.startswith(".")]

    def download_template(self,
                          link: str,
                          version: str | None = None) -> str | None:
        template_name = link.rstrip("/").split("/")[-1]

        if version is not None:
            if self.is_version_exists(template_name, version):
                return None

            version_path = self._version_path(template_name, version)
            os.makedirs(version_path, exist_ok=True)
            try:
                Repo.clone_from(link, version_path, branch=version, depth=1)
                return version
            except Exception:
                shutil.rmtree(version_path, ignore_errors=True)
                return None

        with tempfile.TemporaryDirectory() as tmp_dir:
            clone_path = os.path.join(tmp_dir, "repo")
            try:
                Repo.clone_from(link, clone_path)
            except Exception:
                return None

            portion_file = os.path.join(clone_path, Config.portion_file)
            if not os.path.exists(portion_file):
                return None

            yaml = YAML()
            with open(portion_file, "r") as f:
                data = yaml.load(f)

            version = data.get("version")
            if not version:
                return None

            if self.is_version_exists(template_name, version):
                return None

            version_path = self._version_path(template_name, version)
            os.makedirs(os.path.dirname(version_path), exist_ok=True)
            shutil.move(clone_path, version_path)

        return version

    def delete_if_not_template(self, template_name: str, version: str) -> bool:
        version_path = self._version_path(template_name, version)
        portion_file = os.path.join(version_path, Config.portion_file)
        if not os.path.exists(portion_file):
            shutil.rmtree(version_path)
            template_path = os.path.join(self._pyportion_path, template_name)
            if not os.listdir(template_path):
                shutil.rmtree(template_path)
            return True
        return False

    def delete_template(self, template_name: str, version: str) -> bool:
        version_path = self._version_path(template_name, version)
        if not os.path.exists(version_path):
            return False
        shutil.rmtree(version_path)
        template_path = os.path.join(self._pyportion_path, template_name)
        if not os.listdir(template_path):
            shutil.rmtree(template_path)
        return True

    def get_templates(self) -> list[str]:
        return os.listdir(self._pyportion_path)

    def copy_template(self,
                      template_name: str,
                      version: str,
                      project_name: str) -> None:
        template_path = os.path.join(self._version_path(template_name,
                                                        version),
                                     "base")
        shutil.copytree(src=template_path,
                        dst=project_name,
                        dirs_exist_ok=True)

    def copy_portion(self,
                     template_name: str,
                     version: str,
                     portion_path: list[str],
                     dest_path: list[str]) -> None:
        path = os.path.join(self._version_path(template_name, version),
                            ".portions",
                            *portion_path)
        dest = os.path.join(*dest_path)
        shutil.copyfile(path, dest)

    def read_configuration(self,
                           template_name: str,
                           version: str) -> TemplateConfig:
        path = os.path.join(self._version_path(template_name, version),
                            Config.portion_file)
        yaml = YAML()
        with open(path, "r") as f:
            data = yaml.load(f)
        return TemplateConfig(**data)

    def update_configuration(self,
                             template_name: str,
                             version: str,
                             config: TemplateConfig) -> None:
        path = os.path.join(self._version_path(template_name, version),
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
                          title_style="green bold",
                          expand=False)

            for key, value in data.items():
                table.add_row(
                    f"[bold green]{key.capitalize()}[/]",
                    str(value),
                )
            return table

        metadata_table = build_table(metadata)

        portions_table = None
        if portions:

            portions_table = Table(
                "[bold green]Portions:[/]",
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
            title="[bold green]Template Info[/]",
            border_style="green",
            expand=False
        )
