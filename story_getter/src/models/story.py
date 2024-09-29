from enum import Enum
from sqlalchemy import Column, ForeignKey, String, UniqueConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.alchemy import Base
from models.mixin import IdMixin, TimestampMixin


class StoryType(Enum):
    STORY = 'Story'
    JOKE = 'Joke'


class Story(IdMixin, TimestampMixin, Base):
    __tablename__ = 'stories'

    story_type = Column(Enum(StoryType), unique=True, nullable=False)
    name = Column(String(255), unique=False, nullable=True)
    text = Column(String(), unique=False, nullable=False)

    used_stories = relationship('UsedStories', back_populates='story', lazy='selectin')

    def __repr__(self) -> str:
        return f'<Story {self.name}>'

class UsedStory(IdMixin, TimestampMixin, Base):
    __tablename__ = 'used_stories'

    __table_args__ = (
        UniqueConstraint('story_id', 'used_story_id'),
    )

    story_id = Column(UUID(as_uuid=True),
                     ForeignKey('stories.id', ondelete='CASCADE'),
                     nullable=False)

    used_story_id = Column(UUID(as_uuid=True),
                           ForeignKey('stories.id', ondelete='CASCADE'),
                           nullable=False)

    story = relationship('Story', back_populates='stories', lazy='selectin')
    used_stories = relationship('Story', back_populates='stories', lazy='selectin')
