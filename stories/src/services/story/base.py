import abc
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.story import StoryResponse


class AbstractStoryService(abc.ABC):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    @abc.abstractmethod
    async def get_random_story(self, *args: Any, ** kwargs: Any) -> StoryResponse | BaseException:
        pass
