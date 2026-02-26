import re
from pathlib import Path

from tabulate import tabulate

from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager
from portion.models import Config
from portion.models import Message


class TemplateCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.template_manager = TemplateManager()
        self.project_manager = ProjectManager()
        self.template_manager.create_pyportion_dir()

    def _check_link(self, link: str) -> bool:
        return bool(re.match(r"^https?:\/\/\S+$", link))

    def _resolve_link(self, link: str) -> str:
        if link.startswith("gh"):
            link = link.replace("gh", Config.github_base_url)
        elif link.startswith("gl"):
            link = link.replace("gl", Config.gitlab_base_url)
        return link

    def download(self, link: str | None = None) -> None:
        if link is None:
            self._download_all_from_config()
            return None

        link = self._resolve_link(link)

        if not self._check_link(link):
            raise ValueError(Message.Template.INVALID_LINK)

        template_name = link.split("/")[-1]
        if self.template_manager.is_template_exists(template_name):
            self.terminal.error(Message.Template.TEMPLATE_EXIST)
            return None

        self.template_manager.download_template(link)
        if self.template_manager.delete_if_not_template(template_name):
            self.terminal.error(Message.Template.NOT_PORTION_TEMPLATE)
            return None

        self.terminal.info(Message.Template.DOWNLOADED,
                           template_name=template_name)

    def _download_all_from_config(self) -> None:
        path = Path.cwd()

        self.terminal.pulse(Message.Install.READING_CONFIGURATION)
        config = self.project_manager.read_configuration(path)

        for template in config.templates:
            try:
                self.terminal.pulse(Message.Install.DOWNLOADING_TEMPALTE,
                                    template_name=template.name,
                                    template_link=template.source,
                                    template_version=template.version)

                self.template_manager.download_template(template.source)

                self.terminal.info(Message.Install.DOWNLOADED,
                                   template_name=template.name,
                                   template_version=template.version)

            except Exception:
                self.terminal.error(Message.Install.COULD_NOT_DOWNLOAD,
                                    template_name=template.name,
                                    tempalte_version=template.version)

    def remove(self, template_name: str) -> None:
        if self.template_manager.delete_template(template_name):
            self.terminal.info(Message.Template.TEMPLATE_DELETED,
                               template_name=template_name)
            return None

        self.terminal.error(Message.Template.TEMPLATE_NOT_EXIST,
                            template_name=template_name)

    def list(self) -> None:
        headers = ["Template Name"]
        templates = [(x,)
                     for x in self.template_manager.get_templates()
                     if not x.startswith(".")]

        if not templates:
            self.terminal.error(Message.Template.NO_TEMPLATES)
            return None

        table = tabulate(templates,
                         headers=headers,
                         tablefmt="simple_grid",
                         stralign="left",
                         numalign="center")
        self.terminal.info(table)

    def info(self, template_name: str) -> None:
        if not self.template_manager.is_template_exists(template_name):
            self.terminal.error(Message.Template.TEMPLATE_NOT_EXIST,
                                template_name=template_name)
            return None

        config = self.template_manager.read_configuration(template_name)
        panel = self.template_manager.get_template_info(config)
        self.terminal.print(panel)
