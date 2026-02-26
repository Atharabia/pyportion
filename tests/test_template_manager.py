import os
from pathlib import PosixPath

import pytest
from rich.panel import Panel

from portion.core.template_manager import TemplateManager
from portion.models.template import TemplateConfig
from portion.models.template import TemplatePortion


def test_create_pyportion_dir(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    path = mock_user_data_dir / "pyportion"

    assert os.path.exists(path) is False
    tm.create_pyportion_dir()
    assert os.path.exists(path) is True


def test_download_template(mock_user_data_dir: PosixPath,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_repo_clone(link, template_path) -> None:
        (mock_template_path).mkdir()

    tm = TemplateManager()
    template_name = "pyportion-template"
    mock_template_path = (mock_user_data_dir / "pyportion" / template_name)
    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_repo_clone)

    tm.create_pyportion_dir()
    assert (mock_template_path).exists() is False
    assert tm.is_template_exists(template_name) is False

    tm.download_template("pyportion.com")

    assert (mock_template_path).exists() is True
    assert tm.is_template_exists(template_name) is True


def test_download_template_wrong_link() -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    result = tm.download_template("invalid_link")
    assert result is False


def test_delete_if_not_template(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir()

    assert tm.delete_if_not_template(template_name) is True
    assert template_path.exists() is False

    template_path.mkdir()
    portion_json_path = template_path / ".pyportion.yml"
    portion_json_path.touch()

    assert tm.delete_if_not_template(template_name) is False
    assert template_path.exists() is True


def test_delete_template(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    assert tm.delete_template(template_name) is False

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir()

    assert tm.delete_template(template_name) is True


def test_get_templates(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    assert len(tm.get_templates()) == 0

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir()

    templates = tm.get_templates()
    assert len(templates) == 1
    assert template_name in templates


def test_copy_template(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"
    project_name = "pyportion-project"

    template_path = (mock_user_data_dir / "pyportion" / template_name / "base")
    template_path.mkdir(parents=True)

    pyportion_file_path = (template_path / ".pyportion.yml")
    pyportion_file_path.touch()

    project_path = (mock_user_data_dir / project_name)

    assert project_path.exists() is False
    tm.copy_template(template_name, str(project_path))
    assert project_path.exists() is True
    assert (project_path / ".pyportion.yml").exists() is True


def test_copy_portion(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"
    project_name = "pyportion-project"

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir(parents=True)

    base_path = template_path / "base"
    base_path.mkdir()

    portion_path = template_path / ".portions"
    portion_path.mkdir()

    portion_file_path = portion_path / "portion.py"
    portion_file_path.touch()

    dest_path = mock_user_data_dir / project_name
    assert dest_path.exists() is False
    dest_path.mkdir()

    tm.copy_portion(template_name,
                    portion_path=["portion.py"],
                    dest_path=list(dest_path.parts) + ["portion.py"])

    assert dest_path.exists() is True
    assert (dest_path / "portion.py").exists() is True


def test_read_template_config(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir(parents=True)
    portion_file_path = template_path / ".pyportion.yml"

    config_str = """
    name: Test Template
    source: https://github.com/
    version: 1.0.0
    description: A test template
    author: Test Author
    type: test
    """

    portion_file_path.write_text(config_str)
    config = tm.read_configuration(template_name)

    assert config is not None
    assert config.name == "Test Template"
    assert config.version == "1.0.0"
    assert config.description == "A test template"
    assert config.author == "Test Author"
    assert config.type == "test"


def test_update_configuration(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir(parents=True)
    portion_file_path = template_path / ".pyportion.yml"

    config_str = """
    name: Test Template
    source: https://github.com/
    version: 1.0.0
    description: A test template
    author: Test Author
    type: test
    """

    portion_file_path.write_text(config_str)
    config = tm.read_configuration(template_name)
    assert config is not None
    assert config.author == "Test Author"

    config.author = "Updated Author"
    tm.update_configuration(template_name, config)
    updated_config = tm.read_configuration(template_name)

    assert updated_config is not None
    assert updated_config.author == "Updated Author"


def test_get_template_info(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    template_config = TemplateConfig(
        name="Test Template",
        source="https://github.com/",
        version="1.0.0",
        description="A test template",
        author="Test Author",
        type="test",
        portions=[
            TemplatePortion(name="portion1", steps=[]),
            TemplatePortion(name="portion2", steps=[]),
        ]
    )

    panel = tm.get_template_info(template_config)
    assert isinstance(panel, Panel)
