from pathlib import PosixPath

from typer.testing import CliRunner

from portion.models import Message
from portion.portion import Portion
from tests.utils import create_template
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
