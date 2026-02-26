import os
import shutil
from pathlib import PosixPath
from unittest.mock import patch

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
    assert tm._resolve_link("gh/Atharabia") == "https://github.com/Atharabia"
    assert tm._resolve_link("gl/Atharabia") == "https://gitlab.com/Atharabia"


def test_template_download_invalid_link(mock_user_data_dir: PosixPath,
                                        app: Portion) -> None:
    runner = CliRunner()
    result = runner.invoke(app.cli, ["template", "download", "invalid"])
    assert result.exit_code == 1


def test_template_download_template_exist(mock_user_data_dir: PosixPath,
                                          app: Portion) -> None:
    runner = CliRunner()
    create_template(mock_user_data_dir, "cli-template")
    template_link = "https://github.com/Atharabia/cli-template"

    func = "portion.core.template_manager.TemplateManager.download_template"
    with patch(func) as mock_download:
        mock_download.return_value = None
        result = runner.invoke(
            app.cli, [
                "template", "download", template_link])
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
    assert f"{template_name}@v1.0.0 has been deleted" in output

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


def test_template_info(mock_user_data_dir: PosixPath,
                       app: Portion) -> None:
    runner = CliRunner()
    template_name = "test-template"
    create_template(mock_user_data_dir, template_name)

    result = runner.invoke(app.cli, ["template", "info", template_name])
    assert result.exit_code == 0
    assert template_name in result.stdout


def test_template_info_not_template(mock_user_data_dir: PosixPath,
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

    def mock_download(self, link: str, version=None) -> str | None:
        t_name = link.split("/")[-1]
        version_path = mock_user_data_dir / "pyportion" / t_name / "1.0.0"
        version_path.mkdir(parents=True, exist_ok=True)
        return "v1.0.0"

    monkeypatch.setattr(
        "portion.core.template_manager.TemplateManager.download_template",
        mock_download
    )

    runner = CliRunner()
    template_link = "https://github.com/Atharabia/not-a-template"
    result = runner.invoke(app.cli, ["template", "download", template_link])
    assert result.exit_code == 0

    output = strip_ansi(result.stdout)
    assert Message.Template.NOT_PORTION_TEMPLATE in output


def test_template_download_success(mock_user_data_dir: PosixPath,
                                   monkeypatch: pytest.MonkeyPatch,
                                   app: Portion) -> None:
    """Test successfully downloading a valid portion template."""
    runner = CliRunner()
    template_link = "https://github.com/Atharabia/valid-template"
    template_name = "valid-template"
    version = "v1.0.0"

    def mock_download(self, link: str, ver=None) -> str | None:
        name = link.split("/")[-1]
        version_path = mock_user_data_dir / \
            "pyportion" / name / version.lstrip("v")
        version_path.mkdir(parents=True, exist_ok=True)
        config_file = version_path / ".pyportion.yml"
        config_file.write_text(f"name: {name}\nversion: {version}\n")
        return version

    monkeypatch.setattr(
        "portion.core.template_manager.TemplateManager.download_template",
        mock_download
    )

    result = runner.invoke(app.cli, ["template", "download", template_link])
    assert result.exit_code == 0

    output = strip_ansi(result.stdout)
    assert (f"{template_name}@{version} has been downloaded successfully"
            in output)


def test_template_download_from_config_no_project(app: Portion) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app.cli, ["template", "download"])
        assert result.exit_code == 1


def test_template_download_from_config_no_templates(app: Portion) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        project_name = "test-project"
        runner.invoke(app.cli, ["init", project_name])

        result = runner.invoke(app.cli, ["template", "download"])
        assert result.exit_code == 0


def test_template_download_from_config_one_template(
        mock_user_data_dir: PosixPath, app: Portion) -> None:
    runner = CliRunner()
    template_name = "base-template"
    create_template(mock_user_data_dir, template_name)

    func = "portion.core.template_manager.TemplateManager.download_template"
    with runner.isolated_filesystem():
        project_name = "test-project"
        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)
        shutil.rmtree(mock_user_data_dir / "pyportion" / template_name)

        with patch(func) as mock_download:
            mock_download.return_value = "v1.0.0"

            result = runner.invoke(app.cli, ["template", "download"])
            assert result.exit_code == 0

            message = f"{template_name}@v1.0.0 is successfully downloaded"
            assert message == strip_ansi(result.stdout)
            assert mock_download.called


def test_template_download_from_config_multiple_templates(
        mock_user_data_dir: PosixPath, app: Portion) -> None:
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
        shutil.rmtree(mock_user_data_dir / "pyportion" / base_template)
        shutil.rmtree(mock_user_data_dir / "pyportion" / template1)
        shutil.rmtree(mock_user_data_dir / "pyportion" / template2)

        with patch(func) as mock_download:
            mock_download.return_value = None
            result = runner.invoke(app.cli, ["template", "download"])
            assert result.exit_code == 0
            assert mock_download.call_count == 3


def test_template_download_from_config_failure(mock_user_data_dir: PosixPath,
                                               app: Portion) -> None:
    runner = CliRunner()
    template_name = "base-template"
    create_template(mock_user_data_dir, template_name)
    func = "portion.core.template_manager.TemplateManager.download_template"

    with runner.isolated_filesystem():
        project_name = "test-project"
        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)
        shutil.rmtree(mock_user_data_dir / "pyportion" / template_name)

        with patch(func) as mock_download:
            mock_download.side_effect = Exception()

            result = runner.invoke(app.cli, ["template", "download"])
            assert result.exit_code == 0

            message = f"Could not download {template_name}@v1.0.0"
            assert message == strip_ansi(result.stdout)
