from pathlib import Path

from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager
from portion.models import Message


class RemoveCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.project_manager = ProjectManager()
        self.template_manager = TemplateManager()

    def remove(self, template_name: str) -> None:
        path = Path.cwd()
        self.terminal.pulse(Message.Remove.CHECKING_TEMPLATES)
        config = self.project_manager.read_configuration(path)

        for i, template in enumerate(config.templates):
            if template.name == template_name:
                config.templates.pop(i)
                break
        else:
            self.terminal.error(Message.Remove.TEMPLATE_NOT_FOUND)
            return None

        self.project_manager.update_configuration(path, config)
        self.terminal.info(Message.Remove.TEMPLATE_REMOVED,
                           template_name=template_name)
