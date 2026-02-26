from pydantic import BaseModel


class ProjectTemplate(BaseModel):
    name: str
    source: str
    version: str


class PortionConfig(BaseModel):
    name: str
    templates: list[ProjectTemplate]
