from __future__ import annotations

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

type PyObjectId = Annotated[str, BeforeValidator(str)]

class Project(BaseModel):
    """ Container for a single project """
    id: PyObjectId = Field(alias="_id")
    owner_id: PyObjectId = Field(alias="owner_id")
    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default="Ten projekt nie ma jeszcze opisu.")
    files_id: list[str] | None = Field(default_factory=list)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class UpdateProject(BaseModel):
    """ Container for a single project """
    title: str | None = None
    description: str | None = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class ProjectCollection(BaseModel):
    """ Container for a collection of projects """
    projects: list[Project]
