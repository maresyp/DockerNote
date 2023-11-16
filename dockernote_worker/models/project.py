from __future__ import annotations

from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

type PyObjectId = Annotated[str, BeforeValidator(str)]

class Project(BaseModel):
    """ Container for a single project """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner_id: PyObjectId = Field(alias="owner_id", default=None)
    files_id: list[str] = Field(default_factory=list)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
