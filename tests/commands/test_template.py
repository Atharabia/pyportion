from pathlib import PosixPath

import pytest
from typer.testing import CliRunner

from portion.commands import TemplateCommand
from portion.models import Message
from portion.portion import Portion
from tests.utils import create_template
from tests.utils import strip_ansi


def test_check_link() -> None:
    tm = TemplateCommand()
    assert tm._check_link("https://github.com/") is True
    assert tm._check_link("http://github.com/") is True


def test_resolve_link() -> None:
    tm = TemplateCommand()
    assert tm._resolve_link("gh/pyportion") == "https://github.com/pyportion"
    assert tm._resolve_link("gl/pyportion") == "https://gitlab.com/pyportion"


def test_template_download_invalid_link(mock_user_data_dir: PosixPath,
                                        app: Portion) -> None:
    runner = CliRunner()
    result = runner.invoke(app.cli, ["template", "download", "invalid"])
    assert result.exit_code == 1


def test_template_download_template_exist(mock_user_data_dir: PosixPath,
                                          app: Portion) -> None:
    runner = CliRunner()
    create_template(mock_user_data_dir, "cli-template")
    template_link = "https://github.com/pyportion/cli-template"
    result = runner.invoke(app.cli, ["template", "download", template_link])
    assert result.exit_code == 0
    assert Message.Template.TEMPLATE_EXIST == strip_ansi(result.stdout)


def test_template_command_remove_invalid(mock_user_data_dir: PosixPath,
                                         app: Portion) -> None:
    runner = CliRunner()
    result = runner.invoke(app.cli, ["template", "remove"])
    assert result.exit_code == 2


def test_template_command_remove(mock_user_data_dir: PosixPath,
                                 app: Portion) -> None:
    runner = CliRunner()
    template_name = "test-template"
    create_template(mock_user_data_dir, template_name)

    result = runner.invoke(app.cli, ["template", "remove", template_name])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert f"The template ({template_name}) has been deleted" in output

    result = runner.invoke(app.cli, ["template", "remove", template_name])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert f"The template ({template_name}) is not exist" in output


def test_template_command_list(mock_user_data_dir: PosixPath,
                               app: Portion) -> None:
    runner = CliRunner()
    template_name1 = "test-template-1"
    template_name2 = "test-template-2"
    create_template(mock_user_data_dir, template_name1)
    create_template(mock_user_data_dir, template_name2)

    result = runner.invoke(app.cli, ["template", "list"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert template_name1 in output
    assert template_name2 in output


def test_template_command_list_no_templates(mock_user_data_dir: PosixPath,
                                            app: Portion) -> None:
    runner = CliRunner()
    result = runner.invoke(app.cli, ["template", "list"])
    assert result.exit_code == 0
    assert Message.Template.NO_TEMPLATES in result.stdout


def test_template_command_info(mock_user_data_dir: PosixPath,
                               app: Portion) -> None:
    runner = CliRunner()
    template_name = "test-template"
    create_template(mock_user_data_dir, template_name)

    result = runner.invoke(app.cli, ["template", "info", template_name])
    assert result.exit_code == 0
    assert template_name in result.stdout


def test_template_command_info_not_template(mock_user_data_dir: PosixPath,
                                            app: Portion) -> None:
    runner = CliRunner()
    template_name = "test-template"
    result = runner.invoke(app.cli, ["template", "info", template_name])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert f"The template ({template_name}) is not exist" in output


def test_template_download_not_template(mock_user_data_dir: PosixPath,
                                        monkeypatch: pytest.MonkeyPatch,
                                        app: Portion) -> None:

    def mock_download(self, link: str) -> bool:
        template_name = link.split("/")[-1]
        template_path = mock_user_data_dir / "pyportion" / template_name
        template_path.mkdir(parents=True, exist_ok=True)
        return True

    monkeypatch.setattr(
        "portion.core.template_manager.TemplateManager.download_template",
        mock_download
    )

    runner = CliRunner()
    template_link = "https://github.com/pyportion/not-a-template"
    result = runner.invoke(app.cli, ["template", "download", template_link])
    assert result.exit_code == 0

    output = strip_ansi(result.stdout)
    assert Message.Template.NOT_PORTION_TEMPLATE in output


def test_template_download_success(mock_user_data_dir: PosixPath,
                                   monkeypatch: pytest.MonkeyPatch,
                                   app: Portion) -> None:
    """Test successfully downloading a valid portion template."""
    runner = CliRunner()
    template_link = "https://github.com/pyportion/valid-template"
    template_name = "valid-template"

    def mock_download(self, link: str) -> bool:
        template_name = link.split("/")[-1]
        template_path = mock_user_data_dir / "pyportion" / template_name
        template_path.mkdir(parents=True, exist_ok=True)
        config_file = template_path / ".pyportion.yml"
        config_file.write_text("name: Valid Template\nversion: 1.0.0\n")
        return True

    monkeypatch.setattr(
        "portion.core.template_manager.TemplateManager.download_template",
        mock_download
    )

    result = runner.invoke(app.cli, ["template", "download", template_link])
    assert result.exit_code == 0

    output = strip_ansi(result.stdout)
    assert f"{template_name} has been downloaded successfully" in output
