from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models import StoryType


class StoryResponse(BaseModel):
    id: UUID
    story_type: StoryType
    name: str
    text: str

    model_config = ConfigDict(from_attributes=True)