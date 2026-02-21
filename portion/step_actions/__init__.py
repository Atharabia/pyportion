from portion.base import ActionBase
from portion.core import Logger
from portion.models import ProjectTemplate
from portion.models import TemplatePortionStepsType

from .add_import import AddImportAction
from .add_to_list import AddToListAction
from .ask import AskAction
from .copy import CopyAction
from .replace import ReplaceAction
from .set_var import SetVarAction

all_actions = {
    "add_import": AddImportAction,
    "add_to_list": AddToListAction,
    "ask": AskAction,
    "copy": CopyAction,
    "replace": ReplaceAction,
    "set_var": SetVarAction,
}


def create_action(step: TemplatePortionStepsType,
                  project_template: ProjectTemplate,
                  memory: dict[str, str],
                  logger: Logger) -> ActionBase:
    return all_actions[step.type.value](step, project_template, memory, logger)
