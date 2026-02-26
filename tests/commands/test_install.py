import os
from pathlib import PosixPath
from unittest.mock import patch

from typer.testing import CliRunner

from portion.portion import Portion
from tests.utils import create_template
from tests.utils import strip_ansi


def test_install_command_no_project(app: Portion) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app.cli, ["template", "download"])
        assert result.exit_code == 1


def test_install_command_project_without_templates(app: Portion) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        project_name = "test-project"
        runner.invoke(app.cli, ["init", project_name])

        result = runner.invoke(app.cli, ["template", "download"])
        assert result.exit_code == 0


def test_install_command_with_one_template(mock_user_data_dir: PosixPath,
                                           app: Portion) -> None:
    runner = CliRunner()
    template_name = "base-template"
    create_template(mock_user_data_dir, template_name)

    func = "portion.core.template_manager.TemplateManager.download_template"
    with runner.isolated_filesystem():
        project_name = "test-project"
        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        with patch(func) as mock_download:
            mock_download.return_value = None

            result = runner.invoke(app.cli, ["template", "download"])
            assert result.exit_code == 0

            print(result.stdout)
            message = f"{template_name}@v1.0.0 is successfully downloaded"
            assert message == strip_ansi(result.stdout)
            assert mock_download.called


def test_install_command_with_multiple_templates(mock_user_data_dir: PosixPath,
                                                 app: Portion) -> None:
    runner = CliRunner()
    base_template = "base-template"
    template1 = "template1"
    template2 = "template2"
    create_template(mock_user_data_dir, base_template)
    create_template(mock_user_data_dir, template1)
    create_template(mock_user_data_dir, template2)

    func = "portion.core.template_manager.TemplateManager.download_template"
    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", base_template, project_name])
        os.chdir(project_name)
        runner.invoke(app.cli, ["add", template1])
        runner.invoke(app.cli, ["add", template2])

        with patch(func) as mock_download:
            mock_download.return_value = None
            result = runner.invoke(app.cli, ["template", "download"])
            assert result.exit_code == 0
            assert mock_download.call_count == 3


def test_install_command_download_failure(mock_user_data_dir: PosixPath,
                                          app: Portion) -> None:
    runner = CliRunner()
    template_name = "base-template"
    create_template(mock_user_data_dir, template_name)
    func = "portion.core.template_manager.TemplateManager.download_template"

    with runner.isolated_filesystem():
        project_name = "test-project"
        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        with patch(func) as mock_download:
            mock_download.side_effect = Exception()

            result = runner.invoke(app.cli, ["template", "download"])
            assert result.exit_code == 0

            message = f"Could not donwload {template_name}@v1.0.0"
            assert message == strip_ansi(result.stdout)
