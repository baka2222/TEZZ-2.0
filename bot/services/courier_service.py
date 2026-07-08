from bot.database.models import Category, Shop, Product, Service, Client, Order, OrderItem, CourierOrder, PricingRule, TimeSurcharge
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from bot.database.session import async_session as async_session_maker


class CourierService:
    def __init__(self, session):
        self.session = session

    async def get_client_by_tg(self, tg_id: int) -> Client | None:
        from sqlalchemy import select
        result = await self.session.execute(
            select(Client).where(Client.tg_code == str(tg_id))
        )
        return result.scalar_one_or_none()

    async def get_pricing_rules(self):
        from sqlalchemy import select
        result = await self.session.execute(
            select(PricingRule).order_by(PricingRule.min_distance)
        )
        return result.scalars().all()

    async def get_time_surcharges(self):
        from sqlalchemy import select
        result = await self.session.execute(select(TimeSurcharge))
        return result.scalars().all()

    async def create_courier_order(self, client_id: int, point_a: tuple, point_b: tuple,
                                   comment: str, price: float, distance: float) -> CourierOrder:
        order = CourierOrder(
            client_id=client_id,
            point_a_lat=point_a[0],
            point_a_lng=point_a[1],
            point_b_lat=point_b[0],
            point_b_lng=point_b[1],
            comment=comment,
            status='new',
            price=price,
            distance_km=distance
        )
        self.session.add(order)
        await self.session.commit()
        return order

    async def get_order_by_id(self, order_id: int) -> CourierOrder | None:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        result = await self.session.execute(
            select(CourierOrder)
            .options(selectinload(CourierOrder.client))
            .options(selectinload(CourierOrder.courier))
            .where(CourierOrder.id == order_id)
        )
        return result.scalar_one_or_none()

    async def take_order(self, order_id: int, courier_id: int) -> CourierOrder:
        result = await self.session.execute(
            select(CourierOrder)
            .options(
                selectinload(CourierOrder.client),   # сразу подгружаем client
                selectinload(CourierOrder.courier)   # сразу подгружаем courier
            )
            .where(CourierOrder.id == order_id)
            .with_for_update()
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")
        if order.status != 'new':
            raise ValueError("Order already taken")
        
        order.courier_id = courier_id
        order.status = 'assigned'
        await self.session.commit()
        return order

    async def update_order_status(self, order_id: int, new_status: str):
        from sqlalchemy import update
        await self.session.execute(
            update(CourierOrder)
            .where(CourierOrder.id == order_id)
            .values(status=new_status)
        )
        await self.session.commit()
