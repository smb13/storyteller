import asyncio
from functools import lru_cache

import aiohttp
from bs4 import BeautifulSoup
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.alchemy import get_session
from models import StoryType
from schemas.story import StoryResponse
from services.story.base import AbstractStoryService


class AnekdotRuService(AbstractStoryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.random_stories_url = 'https://www.anekdot.ru/random/story/'
        self.random_jokes_url = 'https://www.anekdot.ru/random/anekdot/'

    async def get_random_story(self, **kwargs) -> StoryResponse | BaseException:
        story_type = kwargs.get('story_type', StoryType.STORY)
        url = self.random_jokes_url if story_type == StoryType.JOKE else self.random_stories_url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, "lxml")
        pass

@lru_cache
def get_anekdot_ru_service(
    alchemy: AsyncSession = Depends(get_session),
) -> AnekdotRuService:
    """Gets AuthService instance for dependencies injection.

    About @lru_cache:
    Each request should get a fresh AsyncSession to avoid sharing transactions
    and to maintain the integrity of the session's state within each request's lifecycle.
    Therefore, caching a service that depends on such a session is not recommended."""

    return AnekdotRuService(session=alchemy)


async def main(anekdot_ru_service: AnekdotRuService = Depends(get_anekdot_ru_service)):
    await anekdot_ru_service.get_random_story()


asyncio.run(main())