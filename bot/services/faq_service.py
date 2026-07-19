from sqlalchemy import select

from bot.database.models import FAQCategory, FAQItem
from bot.services.base import BaseService


class FAQService(BaseService):
    def localized(self, obj, field: str, lang: str) -> str:
        return getattr(obj, f"{field}_{lang}", None) or getattr(obj, field, '') or ''

    async def get_categories(self, app_type: str = 'market_bot') -> list[FAQCategory]:
        result = await self.session.execute(
            select(FAQCategory)
            .where(FAQCategory.app_type == app_type, FAQCategory.is_active.is_(True))
            .order_by(FAQCategory.order, FAQCategory.id)
        )
        return list(result.scalars().all())

    async def get_category(self, category_id: int) -> FAQCategory | None:
        result = await self.session.execute(
            select(FAQCategory).where(FAQCategory.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_items(self, category_id: int) -> list[FAQItem]:
        result = await self.session.execute(
            select(FAQItem)
            .where(FAQItem.category_id == category_id, FAQItem.is_active.is_(True))
            .order_by(FAQItem.order, FAQItem.id)
        )
        return list(result.scalars().all())

    async def get_item(self, item_id: int) -> FAQItem | None:
        result = await self.session.execute(
            select(FAQItem).where(FAQItem.id == item_id)
        )
        return result.scalar_one_or_none()
