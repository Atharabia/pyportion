from pathlib import Path

from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager
from portion.models import Message
from portion.models import ProjectTemplate


class AddCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.project_manager = ProjectManager()
        self.template_manager = TemplateManager()

    def add(self, template_name: str) -> None:
        self.terminal.pulse(Message.Add.CHECKING_TEMPLATE,
                            template_name=template_name)

        if not self.template_manager.is_template_exists(template_name):
            self.terminal.error(Message.Add.TEMPLATE_EXIST)
            return None

        self.terminal.pulse(Message.Add.CHECKING_USED_TEMPLATES)
        path = Path.cwd()
        pconfig = self.project_manager.read_configuration(path)
        for template in pconfig.templates:
            if template.name == template_name:
                self.terminal.error(Message.Add.TEMPLATE_ALREADY_ADDED)
                return None

        versions = self.template_manager.get_template_versions(template_name)
        if len(versions) == 1:
            version = versions[0]
        else:
            version = self.terminal.choose(Message.Add.CHOOSE_VERSION,
                                           versions,
                                           template_name=template_name)

        self.terminal.pulse(Message.Add.VALIDATE_TEMPALTE)
        tconfig = self.template_manager.read_configuration(template_name,
                                                           version)

        self.terminal.pulse(Message.Add.ADDING_TEMPLATE,
                            template_name=template_name)
        pconfig.templates.append(ProjectTemplate(name=tconfig.name,
                                                 source=tconfig.source,
                                                 version=version))

        self.project_manager.update_configuration(path, pconfig)
        self.terminal.info(Message.Add.TEMPLATE_ADDED,
                           template_name=template_name)
