import pytest
from rich.text import Text

from portion.core import Terminal
from portion.models import cli_state

logger = Terminal()


def test_logger_pulse(capsys: pytest.CaptureFixture) -> None:
    cli_state.verbose = True
    logger.pulse("This is a pulse message.")
    captured = capsys.readouterr()
    assert "This is a pulse message." in captured.out


def test_logger_info(capsys: pytest.CaptureFixture) -> None:
    logger.info("This is an info message.")
    captured = capsys.readouterr()
    assert "This is an info message." in captured.out


def test_logger_warn(capsys: pytest.CaptureFixture) -> None:
    logger.warn("This is a warning message.")
    captured = capsys.readouterr()
    assert "This is a warning message." in captured.out


def test_logger_error(capsys: pytest.CaptureFixture) -> None:
    logger.error("This is an error message.")
    captured = capsys.readouterr()
    assert "This is an error message." in captured.out


def test_logger_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr('rich.prompt.Confirm.ask', lambda _: True)
    response = logger.prompt("Do you want to continue?")
    assert response is True

    monkeypatch.setattr('rich.prompt.Confirm.ask', lambda _: False)
    response = logger.prompt("Do you want to continue?")
    assert response is False


def test_logger_print(capsys: pytest.CaptureFixture) -> None:
    text = Text("[bold cyan]This is a printed message.[/]")
    logger.print(text)
    captured = capsys.readouterr()
    assert "This is a printed message." in captured.out


def test_logger_choose(monkeypatch: pytest.MonkeyPatch) -> None:
    choices = ["option_a", "option_b", "option_c"]

    class MockSelect:
        def ask(self):
            return "option_b"

    monkeypatch.setattr("questionary.select",
                        lambda *args, **kwargs: MockSelect())

    result = logger.choose("Pick one:", choices)
    assert result == "option_b"


def test_logger_pulse_non_verbose(capsys: pytest.CaptureFixture) -> None:
    cli_state.verbose = False
    logger = Terminal()
    logger.pulse("This is a pulse message.")
    captured = capsys.readouterr()
    assert "This is a pulse message." not in captured.out
