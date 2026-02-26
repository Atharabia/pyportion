import os
from pathlib import PosixPath

from typer.testing import CliRunner

from portion.commands import BuildCommand
from portion.models.project import ProjectTemplate
from portion.models.template import TemplatePortion
from portion.portion import Portion
from tests.utils import create_template_with_portions
from tests.utils import strip_ansi


def test_find_portion_success() -> None:
    command = BuildCommand()
    template1 = ProjectTemplate(name="template1", source="", version="")
    template2 = ProjectTemplate(name="template2", source="", version="")
    portion1 = TemplatePortion(name="auth", steps=[])
    portion2 = TemplatePortion(name="database", steps=[])
    portion3 = TemplatePortion(name="api", steps=[])

    portions = [
        (template1, portion1),
        (template1, portion2),
        (template2, portion3),
    ]

    result = command._find_portion(portions, "database")
    assert result is not None
    assert result[0] == template1
    assert result[1] == portion2
    assert result[1].name == "database"


def test_find_portion_not_found() -> None:
    command = BuildCommand()
    template1 = ProjectTemplate(name="template1", source="", version="")
    portion1 = TemplatePortion(name="auth", steps=[])
    portions = [(template1, portion1)]

    result = command._find_portion(portions, "none")
    assert result is None


def test_find_portion_empty_list() -> None:
    command = BuildCommand()
    result = command._find_portion([], "any_portion")
    assert result is None


def test_build_command_no_project(app: Portion) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app.cli, ["build", "some-portion"])
        assert result.exit_code == 1


def test_build_command_portion_not_found(mock_user_data_dir: PosixPath,
                                         app: Portion) -> None:
    runner = CliRunner()
    template_name = "base-template"
    create_template_with_portions(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        result = runner.invoke(app.cli, ["build", "none"])
        assert result.exit_code == 0
        assert "There is no portion called none" == strip_ansi(result.stdout)


def test_build_command_abort(mock_user_data_dir: PosixPath,
                             app: Portion) -> None:
    runner = CliRunner()
    template_name = "test-template"

    create_template_with_portions(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        result = runner.invoke(app.cli, ["build", "feature1"], input="n\n")
        assert result.exit_code == 0
        assert "Aborted" in strip_ansi(result.stdout)


def test_build_command_success_with_auto_confirm(mock_user_data_dir: PosixPath,
                                                 app: Portion) -> None:
    runner = CliRunner()
    template_name = "test-template"

    create_template_with_portions(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        result = runner.invoke(app.cli, ["-y", "build", "feature1"])
        assert result.exit_code == 0
        assert os.path.exists("feature1.py")


def test_build_command_multiple_portions(mock_user_data_dir: PosixPath,
                                         app: Portion) -> None:
    runner = CliRunner()
    template_name = "multi-portion-template"

    create_template_with_portions(mock_user_data_dir, template_name)

    with runner.isolated_filesystem():
        project_name = "test-project"

        runner.invoke(app.cli, ["new", template_name, project_name])
        os.chdir(project_name)

        result1 = runner.invoke(app.cli, ["-y", "build", "feature1"])
        assert result1.exit_code == 0
        assert os.path.exists("feature1.py")

        result2 = runner.invoke(app.cli, ["-y", "build", "feature2"])
        assert result2.exit_code == 0
        assert os.path.exists("feature1.py")
        assert os.path.exists("feature2.py")
