import subprocess
from unittest.mock import MagicMock

import pytest

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateBashCommand
from portion.models import cli_state
from portion.step_actions import BashAction


def make_bash_action(command: str = "echo hello",
                     variable: str = "output") -> BashAction:
    return BashAction(
        step=TemplateBashCommand(
            type=ActionType.BASH,
            command=command,
            variable=variable,
        ),
        project_template=ProjectTemplate(name="Test", source="", version=""),
        memory={},
        terminal=Terminal(),
    )


def test_bash_action_prepare():
    action = make_bash_action()
    action.prepare()


def test_bash_action_apply_auto_confirm(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli_state, "auto_confirm", True)
    mock_result = MagicMock()
    mock_result.stdout = "hello\n"
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: mock_result)

    action = make_bash_action()
    action.apply()

    assert action.memory["output"] == "hello\n"


def test_bash_action_apply_abort(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli_state, "auto_confirm", False)
    monkeypatch.setattr("portion.core.terminal.Terminal.prompt",
                        lambda self, *args, **kwargs: False)

    action = make_bash_action()
    action.apply()

    assert "output" not in action.memory


def test_bash_action_apply_confirmed(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli_state, "auto_confirm", False)
    monkeypatch.setattr("portion.core.terminal.Terminal.prompt",
                        lambda self, *args, **kwargs: True)
    mock_result = MagicMock()
    mock_result.stdout = "world\n"
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: mock_result)

    action = make_bash_action()
    action.apply()

    assert action.memory["output"] == "world\n"
