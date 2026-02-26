from pathlib import Path

from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager


class InfoCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.template_manager = TemplateManager()
        self.project_manager = ProjectManager()

    def info(self) -> None:
        path = Path.cwd()
        config = self.project_manager.read_configuration(path)
        templates = {t.name: self.template_manager.read_configuration(t.name)
                     for t in config.templates}

        panel = self.project_manager.get_project_info(config, templates)
        self.terminal.print(panel)
