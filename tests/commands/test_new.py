from pathlib import PosixPath

import pytest
from typer.testing import CliRunner

from portion.models import Message
from portion.portion import Portion
from tests.utils import create_template
from tests.utils import create_template_with_setup
from tests.utils import create_template_with_setup_and_conditional
from tests.utils import create_template_with_two_versions
from tests.utils import create_template_without_source


def test_new_command_with_wrong_template(app: Portion) -> None:
    runner = CliRunner()
    result = runner.invoke(app.cli, ["new", "template", "project"])
    assert result.exit_code == 0
    assert Message.New.TEMPLATE_NOT_EXIST in result.stdout


def test_new_command_project_exist(mock_user_data_dir: PosixPath,
                                   app: Portion) -> None:
    runner = CliRunner()
    template_name = "cli-template"
    create_template(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        result = runner.invoke(app.cli, ["new", template_name, project_name])
        assert result.exit_code == 0
        assert Message.New.PROJECT_EXIST not in result.stdout

        result = runner.invoke(app.cli, ["new", template_name, project_name])
        assert result.exit_code == 0
        assert Message.New.PROJECT_EXIST in result.stdout


def test_new_command_template_without_source(mock_user_data_dir: PosixPath,
                                             app: Portion) -> None:
    runner = CliRunner()
    template_name = "cli-template"
    create_template_without_source(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        result = runner.invoke(app.cli, ["new", template_name, project_name])
        assert result.exit_code == 1


def test_new_command_choose_version(mock_user_data_dir: PosixPath,
                                    app: Portion,
                                    monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CliRunner()
    template_name = "multi-version-template"
    create_template_with_two_versions(mock_user_data_dir, template_name)

    monkeypatch.setattr("portion.core.terminal.Terminal.choose",
                        lambda self, *args, **kwargs: "v1.0.0")

    with runner.isolated_filesystem():
        result = runner.invoke(app.cli, ["new", template_name, "test-project"])
        assert result.exit_code == 0
        assert "test-project" in result.stdout


def test_new_command_with_setup(mock_user_data_dir: PosixPath,
                                app: Portion) -> None:
    runner = CliRunner()
    template_name = "setup-template"
    create_template_with_setup(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        result = runner.invoke(app.cli, ["new", template_name, "test-project"])
        assert result.exit_code == 0
        assert "test-project" in result.stdout


def test_new_command_with_setup_verbose_skip(mock_user_data_dir: PosixPath,
                                             app: Portion,
                                             ) -> None:
    runner = CliRunner()
    template_name = "cond-setup-template"
    create_template_with_setup_and_conditional(
        mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        result = runner.invoke(
            app.cli, [
                "-v", "new", template_name, "test-project"])
        assert result.exit_code == 0
        assert Message.New.SKIP_SETUP_STEP.split(":")[0] in result.stdout
