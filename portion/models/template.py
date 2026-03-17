from enum import Enum
from typing import Union

from pydantic import BaseModel


class ActionType(Enum):
    ADD_IMPORT = "add_import"
    ADD_PORTION = "add_portion"
    ADD_TO_LIST = "add_to_list"
    ASK = "ask"
    COPY = "copy"
    REPLACE = "replace"
    SET_VAR = "set_var"


class TemplateAddImportAction(BaseModel):
    type: ActionType
    path: list[str]
    import_statement: str


class TemplateAddPortionAction(BaseModel):
    type: ActionType
    path: list[str]
    value: str


class TemplateAddToListAction(BaseModel):
    type: ActionType
    path: list[str]
    list_name: str
    value: str | int | float | bool


class TemplateAskAction(BaseModel):
    type: ActionType
    question: str
    variable: str


class TemplateCopyAction(BaseModel):
    type: ActionType
    from_path: list[str]
    to_path: list[str]


class TemplateReplacement(BaseModel):
    keyword: str
    value: str
    mode: str


class TemplateReplaceAction(BaseModel):
    type: ActionType
    path: list[str]
    replacements: list[TemplateReplacement]


class TemplateSetVarAction(BaseModel):
    type: ActionType
    key: str
    value: str
    mode: str | None = None


TemplatePortionStepsType = Union[
    TemplateAddImportAction,
    TemplateAddToListAction,
    TemplateAskAction,
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

    portions: list[TemplatePortion] = []
