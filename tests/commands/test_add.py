import os
from pathlib import PosixPath

from typer.testing import CliRunner

from portion.models import Message
from portion.portion import Portion
from tests.utils import create_template
from tests.utils import create_template_without_source
from tests.utils import strip_ansi


def test_add_command_no_project(app: Portion) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app.cli, ["add", "some-template"])
        assert result.exit_code == 0


def test_add_command_template_not_exist(mock_user_data_dir: PosixPath,
                                        app: Portion) -> None:
    runner = CliRunner()
    template_name = "base-template"
    create_template(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        result = runner.invoke(app.cli, ["add", "non-existent-template"])
        assert result.exit_code == 0
        assert Message.Add.TEMPLATE_EXIST in result.stdout


def test_add_command_template_without_source(mock_user_data_dir: PosixPath,
                                             app: Portion) -> None:
    runner = CliRunner()
    base_template = "base-template"
    incomplete_template = "incomplete-template"
    create_template(mock_user_data_dir, base_template)
    create_template_without_source(mock_user_data_dir, incomplete_template)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", base_template, project_name])
        os.chdir(project_name)

        result = runner.invoke(app.cli, ["add", incomplete_template])
        assert result.exit_code == 1


def test_add_command_success(mock_user_data_dir: PosixPath,
                             app: Portion) -> None:
    runner = CliRunner()
    base_template = "base-template"
    additional_template = "additional-template"
    create_template(mock_user_data_dir, base_template)
    create_template(mock_user_data_dir, additional_template)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", base_template, project_name])
        os.chdir(project_name)

        result = runner.invoke(app.cli, ["add", additional_template])
        assert result.exit_code == 0
        message = f"({additional_template}) has been added successfully"
        assert message == strip_ansi(result.stdout)


def test_add_command_template_already_added(mock_user_data_dir: PosixPath,
                                            app: Portion) -> None:
    runner = CliRunner()
    base_template = "base-template"
    additional_template = "additional-template"
    create_template(mock_user_data_dir, base_template)
    create_template(mock_user_data_dir, additional_template)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", base_template, project_name])
        os.chdir(project_name)

        runner.invoke(app.cli, ["add", additional_template])
        result = runner.invoke(app.cli, ["add", additional_template])
        assert result.exit_code == 0
        assert Message.Add.TEMPLATE_ALREADY_ADDED in result.stdout


def test_add_command_multiple_templates(mock_user_data_dir: PosixPath,
                                        app: Portion) -> None:
    runner = CliRunner()
    base_template = "base-template"
    template1 = "template1"
    template2 = "template2"
    create_template(mock_user_data_dir, base_template)
    create_template(mock_user_data_dir, template1)
    create_template(mock_user_data_dir, template2)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", base_template, project_name])
        os.chdir(project_name)

        result1 = runner.invoke(app.cli, ["add", template1])
        assert result1.exit_code == 0

        result2 = runner.invoke(app.cli, ["add", template2])
        assert result2.exit_code == 0

        info_result = runner.invoke(app.cli, ["info"])
        assert info_result.exit_code == 0
        assert base_template in info_result.stdout
        assert template1 in info_result.stdout
        assert template2 in info_result.stdout
