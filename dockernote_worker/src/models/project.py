from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

type PyObjectId = Annotated[str, BeforeValidator(str)]

class Project(BaseModel):
    """ Container for a single project """
    id: PyObjectId = Field(alias="_id")
    owner_id: PyObjectId = Field(alias="owner_id")
    files_id: Optional[list[str]] = Field(default_factory=list)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class ProjectCollection(BaseModel):
    """ Container for a collection of projects """
    projects: list[Project] = Field(default_factory=list)
