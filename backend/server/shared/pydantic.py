from typing import Any, Generic, Self, TypeVar

from pydantic import (
    BaseModel as PydanticBaseModel,
)
from pydantic import (
    ConfigDict,
)
from pydantic import (
    Field as _Field,
)

# Re-export Field from pydantic so that people importing BaseModel from here
# don't need to import Field from pydantic
Field = _Field

T = TypeVar("T", bound="BaseModel")


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    def update_key(self, key: str, value: Any) -> Self:
        """
        We use frozen=True so our Pydantic models are immutable. This is a helper
        method that will clone the object and update the given key with the new
        value.
        """
        self_dict = self.model_dump()
        self_dict[key] = value
        return self.model_validate(self_dict)


class PEmpty(BaseModel):
    pass


PListT = TypeVar("PListT", bound=BaseModel)


class PList(BaseModel, Generic[PListT]):
    data: list[PListT]
