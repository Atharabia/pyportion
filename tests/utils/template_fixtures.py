from pathlib import PosixPath

from portion.core import TemplateManager

VERSION = "v1.0.0"
VERSION_DIR = VERSION.lstrip("v")


def create_template(mock_user_data_dir: PosixPath,
                    template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template
    author: Test Author
    type: test
    """
    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()


def create_template_without_source(mock_user_data_dir: PosixPath,
                                   template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    version: {VERSION}
    description: A test template without source
    author: Test Author
    type: test
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()


def create_template_with_portions(mock_user_data_dir: PosixPath,
                                  template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template with multiple portions
    author: Test Author
    type: test
    portions:
      - name: feature1
        steps:
          - type: copy
            from_path: ["feature1.py"]
            to_path: ["feature1.py"]
      - name: feature2
        steps:
          - type: copy
            from_path: ["feature2.py"]
            to_path: ["feature2.py"]
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()

    portions_dir = version_path / ".portions"
    portions_dir.mkdir()
    (portions_dir / "feature1.py").write_text("# Feature 1")
    (portions_dir / "feature2.py").write_text("# Feature 2")
