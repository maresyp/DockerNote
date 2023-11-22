from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

type PyObjectId = Annotated[str, BeforeValidator(str)]

class File(BaseModel):
    """ Container for a single project """
    name: str = Field(alias="name")
    content: str = Field(alias="content")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class FileCollection(BaseModel):
    """ Container for a collection of projects """
    files: list[File] = Field(default_factory=list)
