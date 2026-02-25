from pytest import MonkeyPatch

from portion.core import Terminal
from portion.models import OperationTypes
from portion.models import ProjectTemplate
from portion.models import TemplateAskStep
from portion.step_actions import AskAction

ask_action = AskAction(
    step=TemplateAskStep(
        type=OperationTypes.ASK,
        question="What is your name?",
        variable="name"
    ),
    project_template=ProjectTemplate(name="Sample Template",
                                     link="",
                                     tag=""),
    memory={},
    logger=Terminal()
)


def test_ask_action_prepare(monkeypatch: MonkeyPatch):
    inputs = iter(["PyPortion"])

    def mock_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)
    ask_action.prepare()

    assert ask_action.memory["name"] == "PyPortion"


def test_ask_action_apply():
    ask_action.apply()
