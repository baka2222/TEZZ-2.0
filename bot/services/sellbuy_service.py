from datetime import datetime, timedelta, timezone
from decimal import Decimal

from bot.database.models import Client, TeziksTransaction
from bot.services.base import BaseService


class SellBuyService(BaseService):
    async def get_client_phone(self, tg_id: int) -> str:
        client = await self.get_client_by_tg(tg_id)
        return client.phone if client and client.phone else "Не указан"

    async def set_next_ability(self, client_id: int, field_name: str, days: int = 4):
        client = await self.session.get(Client, client_id)
        if client:
            setattr(client, field_name, datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=days))
            await self.session.commit()

    async def set_next_subscription_disable(self, client_id: int, days: int = 30):
        client = await self.session.get(Client, client_id)
        if client:
            client.next_subscription_disable = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=days)
            await self.session.commit()

    async def clear_next_ability_for_category(self, tg_id: int, category_slug: str) -> Client | None:
        from bot.channels import SLUG_TO_CATEGORY, CHANNELS
        category = SLUG_TO_CATEGORY.get(category_slug)
        if not category:
            return None
        client = await self.get_client_by_tg(tg_id)
        if not client:
            client = Client(tg_code=str(tg_id))
            self.session.add(client)
            await self.session.flush()
        field = CHANNELS[category]["cooldown_field"]
        setattr(client, field, None)
        await self.session.commit()
        return client

    async def save_client(self, name: str, phone: str, tg_code: str, username: str, language: str):
        client = await self.get_client_by_tg(tg_code)
        if not client:
            client = Client(
                name=name,
                phone=phone,
                tg_code=tg_code,
                username=username,
                language=language
            )
            self.session.add(client)
        else:
            client.name = name
            client.phone = phone
            client.username = username
            client.language = language
        await self.session.commit()
        return client
    
    async def ban_client(self, tg_id: int):
        client = await self.get_client_by_tg(tg_id)
        if not client:
            raise ValueError('Client not found')
        client.is_banned = True
        await self.session.commit()
        return client
    
    async def replenishment_balance(self, tg_id: int, amount: Decimal):
        client = await self.get_client_by_tg(tg_id)
        if not client:
            raise ValueError('Client not found')
        client.balance += amount
        await self.session.commit()
        return client
    
    async def deduct_balance(self, tg_id: int, amount: Decimal):
        client = await self.get_client_by_tg(tg_id)
        if not client:
            raise ValueError('Client not found')
        if client.balance < amount:
            raise ValueError('Insufficient balance')
        client.balance -= amount
        await self.session.commit()
        return client
    
    async def send_teziks(self, sender_tg_id: int, receiver_tg_id: int, amount: Decimal):
        sender = await self.get_client_by_tg(sender_tg_id)
        receiver = await self.get_client_by_tg(receiver_tg_id)
        if not sender or not receiver:
            raise ValueError('One or both clients not found')
        if sender.balance < amount:
            raise ValueError('Insufficient balance')
        sender.balance -= amount
        receiver.balance += amount
        self.session.add(TeziksTransaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=amount
        ))
        await self.session.commit()
        return {'status': 'success', 'sender': sender, 'receiver': receiver}