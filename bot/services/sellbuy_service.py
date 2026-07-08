from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import Client
from bot.database.session import async_session as async_session_maker
from datetime import datetime, timedelta, timezone

class SellBuyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_client_by_tg(self, tg_id: int) -> Client | None:
        result = await self.session.execute(
            select(Client).where(Client.tg_code == str(tg_id))
        )
        return result.scalar_one_or_none()

    async def get_client_phone(self, tg_id: int) -> str:
        client = await self.get_client_by_tg(tg_id)
        return client.phone if client and client.phone else "Не указан"

    async def set_next_ability(self, client_id: int, field_name: str):
        """Устанавливает время следующей возможности через 3 дня"""
        # field_name соответствует полю в модели Client: next_ability, next_ability_beauty и т.д.
        # Обновляем через прямое присвоение и commit
        client = await self.session.get(Client, client_id)
        if client:
            setattr(client, field_name, datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=4))
            await self.session.commit()

    async def set_next_subscription_disable(self, client_id: int, days: int):
        """Устанавливает время отключения подписки через указанное количество дней"""
        client = await self.session.get(Client, client_id)
        if client:
            client.next_subscription_disable = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30)
            await self.session.commit()

    async def clear_next_ability_for_category(self, tg_id: int, category_slug: str) -> Client | None:
        """Очищает поле cooldown для указанной категории (после оплаты)"""
        from bot.handlers.sellbuy import SLUG_TO_CATEGORY, CHANNELS  # импорт здесь, чтобы избежать циклического импорта
        category = SLUG_TO_CATEGORY.get(category_slug)
        if not category:
            return None
        client = await self.get_client_by_tg(tg_id)
        if not client:
            # создаём клиента, если не существует (на случай оплаты без регистрации)
            client = Client(tg_code=str(tg_id))
            self.session.add(client)
            await self.session.flush()
        field = CHANNELS[category]["cooldown_field"]
        setattr(client, field, None)
        await self.session.commit()
        return client

    async def get_user_lang(self, tg_id: int) -> str:
        client = await self.get_client_by_tg(tg_id)
        return client.language if client and client.language else 'ru'