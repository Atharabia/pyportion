
from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models.template import TemplateAskAction
from portion.step_actions import create_action
from portion.step_actions.ask import AskAction


def test_create_ask_action():
    step = TemplateAskAction(
        type=ActionType.ASK,
        question="What is your name?",
        variable="user_name"
    )
    project_template = ProjectTemplate(name="Test Template",
                                       source="", version="")
    memory: dict[str, str] = {}
    logger = Terminal()
    action = create_action(step, project_template, memory, logger)
    assert isinstance(action, AskAction)
