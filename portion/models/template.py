from enum import Enum
from typing import Union

from pydantic import BaseModel
from pydantic import Field


class ActionType(Enum):
    ADD_IMPORT = "add_import"
    ADD_PORTION = "add_portion"
    ADD_TO_LIST = "add_to_list"
    ASK = "ask"
    ASK_OPTIONS = "ask_options"
    BASH = "bash"
    COPY = "copy"
    REPLACE = "replace"
    SET_VAR = "set_var"


class TemplateMixin(BaseModel):
    type: ActionType
    when: str | None = None


class TemplateAddImportAction(TemplateMixin):
    path: list[str]
    import_statement: str


class TemplateAddPortionAction(TemplateMixin):
    path: list[str]
    value: str


class TemplateAddToListAction(TemplateMixin):
    path: list[str]
    list_name: str
    value: str | int | float | bool
    as_identifier: bool = False


class TemplateAskAction(TemplateMixin):
    question: str
    variable: str


class TemplateAskOptionsAction(TemplateMixin):
    question: str
    variable: str
    options: list[str] = Field(min_length=1)


class TemplateBashCommand(TemplateMixin):
    command: str
    variable: str


class TemplateCopyAction(TemplateMixin):
    from_path: list[str]
    to_path: list[str]


class TemplateReplacement(BaseModel):
    keyword: str
    value: str
    mode: str


class TemplateReplaceAction(TemplateMixin):
    path: list[str]
    replacements: list[TemplateReplacement]


class TemplateSetVarAction(TemplateMixin):
    key: str
    value: str
    mode: str | None = None


TemplatePortionStepsType = Union[
    TemplateAddImportAction,
    TemplateAddPortionAction,
    TemplateAddToListAction,
    TemplateAskAction,
    TemplateAskOptionsAction,
    TemplateBashCommand,
    TemplateCopyAction,
    TemplateReplaceAction,
    TemplateSetVarAction,
]


class TemplatePortion(BaseModel):
    name: str
    steps: list[TemplatePortionStepsType]


class TemplateConfig(BaseModel):
    name: str
    source: str
    version: str
    description: str
    author: str
    type: str

    setup: list[TemplatePortion] = []
    portions: list[TemplatePortion] = []
