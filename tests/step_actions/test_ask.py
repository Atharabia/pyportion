from pytest import MonkeyPatch

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateAskAction
from portion.models import TemplateAskOptionsAction
from portion.step_actions import AskAction
from portion.step_actions import AskOptionsAction

ask_action = AskAction(
    step=TemplateAskAction(
        type=ActionType.ASK,
        question="What is your name?",
        variable="name"
    ),
    project_template=ProjectTemplate(name="Sample Template",
                                     source="",
                                     version=""),
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


ask_options_action = AskOptionsAction(
    step=TemplateAskOptionsAction(
        type=ActionType.ASK_OPTIONS,
        question="Pick a framework:",
        variable="framework",
        options=["django", "flask", "fastapi"],
    ),
    project_template=ProjectTemplate(name="Sample Template",
                                     source="",
                                     version=""),
    memory={},
    logger=Terminal()
)


def test_ask_options_action_prepare(monkeypatch: MonkeyPatch):
    class MockSelect:
        def ask(self):
            return "flask"

    monkeypatch.setattr("questionary.select",
                        lambda *args, **kwargs: MockSelect())

    ask_options_action.prepare()

    assert ask_options_action.memory["framework"] == "flask"


def test_ask_options_action_apply():
    ask_options_action.apply()
