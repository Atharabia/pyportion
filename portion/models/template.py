from enum import Enum
from typing import Optional
from typing import Union

from pydantic import BaseModel


class OperationTypes(Enum):
    ADD_IMPORT = "add_import"
    ADD_TO_LIST = "add_to_list"
    ASK = "ask"
    COPY = "copy"
    REPLACE = "replace"
    SET_VAR = "set_var"


class TemplateAddImportStep(BaseModel):
    type: OperationTypes
    path: list[str]
    import_statement: str


class TemplateAddToListStep(BaseModel):
    type: OperationTypes
    path: list[str]
    list_name: str
    value: str | int | float | bool


class TemplateAskStep(BaseModel):
    type: OperationTypes
    question: str
    variable: str


class TemplateCopyStep(BaseModel):
    type: OperationTypes
    from_path: list[str]
    to_path: list[str]


class TemplateReplacement(BaseModel):
    keyword: str
    value: str
    mode: str


class TemplateReplaceStep(BaseModel):
    type: OperationTypes
    path: list[str]
    replacements: list[TemplateReplacement]


class TemplateSetVar(BaseModel):
    type: OperationTypes
    key: str
    value: str
    mode: str | None = None


TemplatePortionStepsType = Union[
    TemplateAddImportStep,
    TemplateAddToListStep,
    TemplateAskStep,
    TemplateCopyStep,
    TemplateReplaceStep,
    TemplateSetVar,
]


class TemplatePortion(BaseModel):
    name: str
    steps: list[TemplatePortionStepsType]


class TemplateSource(BaseModel):
    link: str
    tag: str


class TemplateConfig(BaseModel):
    name: str
    version: str
    description: str
    author: str
    type: str

    source: Optional[TemplateSource] = None
    portions: list[TemplatePortion] = []
