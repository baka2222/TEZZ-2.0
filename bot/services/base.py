from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Client


class BaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_client_by_tg(self, tg_id: int) -> Client | None:
        result = await self.session.execute(
            select(Client).where(Client.tg_code == str(tg_id))
        )
        return result.scalar_one_or_none()

    async def get_user_lang(self, tg_id: int) -> str:
        client = await self.get_client_by_tg(tg_id)
        return client.language if client and client.language else 'ru'

    async def set_language(self, tg_id: int, lang_code: str) -> None:
        await self.session.execute(
            update(Client)
            .where(Client.tg_code == str(tg_id))
            .values(language=lang_code)
        )
        await self.session.commit()
