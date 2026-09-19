from datetime import datetime
from hashlib import md5
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from .models import Link
from sqlalchemy.exc import IntegrityError


class LinkRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(self.__class__.__name__)

    async def add_link(self, url: str) -> Link:
        link = Link(url=url)
        self.session.add(link)
        try:
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(link)  
        except IntegrityError:
            await self.session.rollback()
            stmt = select(Link).where(Link.url == url).limit(1)
            link = (await self.session.execute(stmt)).scalar()
        return link

    async def get_link(self, id: int) -> Link | None:
        return await self.session.get(Link, id)

    async def delete_link(self, id: int):
        link = await self.get_link(id)
        if link:
            try:
                await self.session.delete(link)
                await self.session.commit()
            except IntegrityError:
                await self.session.rollback()

    async def get_links(self) -> list[Link]:
        return list((await self.session.execute(select(Link))).scalars())