from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select, or_, and_, delete, insert, func
from sqlalchemy.orm import selectinload

from bot.database.models import Client, ClientAd, TeziksTransaction, client_favorites
from bot.services.base import BaseService


class ProfileService(BaseService):
    async def create_ad(self, client_id: int, category_slug: str,
                        subcategory_slug: str, name: str, description: str,
                        status_label: str, show_phone: bool, price: int,
                        channel_id: int, message_id: int, full_message_ids: list[int],
                        currency: str = 'KGS') -> ClientAd:
        ad = ClientAd(
            client_id=client_id,
            category_slug=category_slug,
            subcategory_slug=subcategory_slug,
            name=name,
            description=description,
            status_label=status_label,
            show_phone=show_phone,
            price=price,
            currency=currency,
            channel_id=channel_id,
            message_id=message_id,
            full_message_ids=full_message_ids,
            status='active'
        )
        self.session.add(ad)
        await self.session.commit()
        return ad

    async def get_client_ads(self, client_id: int) -> list[ClientAd]:
        result = await self.session.execute(
            select(ClientAd)
            .where(ClientAd.client_id == client_id)
            .order_by(ClientAd.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_active_ads(self, client_id: int) -> int:
        result = await self.session.execute(
            select(func.count(ClientAd.id)).where(
                ClientAd.client_id == client_id,
                ClientAd.status == 'active'
            )
        )
        return result.scalar() or 0
    
    async def delete_ad(self, ad_id: int) -> bool:
        result = await self.session.execute(
            select(ClientAd).where(ClientAd.id == ad_id)
        )
        ad = result.scalar_one_or_none()
        
        if not ad:
            return False
        
        await self.session.delete(ad)
        await self.session.commit()

        return True

    async def get_ad(self, ad_id: int) -> ClientAd | None:
        result = await self.session.execute(
            select(ClientAd)
            .options(selectinload(ClientAd.client))
            .where(ClientAd.id == ad_id)
        )
        return result.scalar_one_or_none()

    async def find_ad_by_message(self, channel_id: int,
                                 message_id: int) -> ClientAd | None:
        result = await self.session.execute(
            select(ClientAd)
            .options(selectinload(ClientAd.client))
            .where(
                ClientAd.channel_id == channel_id,
                ClientAd.message_id == message_id
            )
        )
        return result.scalar_one_or_none()

    async def update_ad(self, ad_id: int, **fields) -> ClientAd | None:
        ad = await self.get_ad(ad_id)
        if not ad:
            return None
        for key, value in fields.items():
            setattr(ad, key, value)
        await self.session.commit()
        return ad

    async def deactivate_ad(self, ad_id: int) -> ClientAd | None:
        return await self.update_ad(ad_id, status='inactive')

    async def get_favorites(self, client_id: int) -> list[ClientAd]:
        result = await self.session.execute(
            select(ClientAd)
            .join(client_favorites, client_favorites.c.clientad_id == ClientAd.id)
            .where(client_favorites.c.client_id == client_id)
            .order_by(ClientAd.created_at.desc())
        )
        return list(result.scalars().all())

    async def is_favorite(self, client_id: int, ad_id: int) -> bool:
        result = await self.session.execute(
            select(client_favorites.c.id).where(
                and_(
                    client_favorites.c.client_id == client_id,
                    client_favorites.c.clientad_id == ad_id
                )
            )
        )
        return result.first() is not None

    async def add_favorite(self, client_id: int, ad_id: int) -> bool:
        if await self.is_favorite(client_id, ad_id):
            return False
        await self.session.execute(
            insert(client_favorites).values(client_id=client_id, clientad_id=ad_id)
        )
        await self.session.commit()
        return True

    async def remove_favorite(self, client_id: int, ad_id: int) -> None:
        await self.session.execute(
            delete(client_favorites).where(
                and_(
                    client_favorites.c.client_id == client_id,
                    client_favorites.c.clientad_id == ad_id
                )
            )
        )
        await self.session.commit()

    async def get_transactions(self, client_id: int,
                               limit: int = 15) -> list[TeziksTransaction]:
        result = await self.session.execute(
            select(TeziksTransaction)
            .options(
                selectinload(TeziksTransaction.sender),
                selectinload(TeziksTransaction.receiver)
            )
            .where(
                or_(
                    TeziksTransaction.sender_id == client_id,
                    TeziksTransaction.receiver_id == client_id
                )
            )
            .order_by(TeziksTransaction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_client_name(self, tg_id: int, name: str):
        client = await self.get_client_by_tg(tg_id)
        if client:
            client.name = name
            await self.session.commit()
        return client

    async def update_client_phone(self, tg_id: int, phone: str):
        client = await self.get_client_by_tg(tg_id)
        if client:
            client.phone = phone
            await self.session.commit()
        return client

    async def try_charge(self, client_id: int, amount) -> bool:
        client = await self.session.get(Client, client_id)
        amount = Decimal(str(amount))
        if not client or client.balance < amount:
            return False
        client.balance -= amount
        await self.session.commit()
        return True

    async def add_balance(self, client_id: int, amount):
        client = await self.session.get(Client, client_id)
        if client:
            client.balance += Decimal(str(amount))
            await self.session.commit()
        return client

    async def extend_subscription(self, client_id: int, days: int):
        client = await self.session.get(Client, client_id)
        if not client:
            return None
        base = client.next_subscription_disable
        
        if base and base.tzinfo is not None:
            base = base.replace(tzinfo=None)
        now = datetime.utcnow()

        if base and base > now:
            client.next_subscription_disable = base + timedelta(days=days)
        else:
            client.next_subscription_disable = now + timedelta(days=days)
        await self.session.commit()
        return client
