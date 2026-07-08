from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from bot.database.models import (Category, Shop, Product, Service, Client,
                                 Order, OrderItem, CourierOrder, ProductImage)


class ShopService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_localized(self, obj, field: str, lang: str):
        localized_field = f"{field}_{lang}"
        return getattr(obj, localized_field, None) or getattr(obj, field, "")

    async def get_client_by_tg(self, tg_id: int):
        result = await self.session.execute(
            select(Client).where(Client.tg_code == str(tg_id))
        )
        return result.scalar_one_or_none()

    async def get_categories(self):
        result = await self.session.execute(select(Category).order_by(Category.name))
        return result.scalars().all()

    async def get_shops_by_category(self, cat_id: int):
        result = await self.session.execute(
            select(Shop).where(Shop.category_id == cat_id)
        )
        return result.scalars().all()

    async def get_shop_by_id(self, shop_id: int):
        result = await self.session.execute(
            select(Shop).options(selectinload(Shop.owner)).where(Shop.id == shop_id)
        )
        return result.scalar_one_or_none()

    async def get_product_by_id(self, product_id: int):
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_service_by_id(self, service_id: int):
        result = await self.session.execute(
            select(Service).where(Service.id == service_id)
        )
        return result.scalar_one_or_none()

    async def get_products(self, shop_id: int):
        result = await self.session.execute(
            select(Product).where(Product.shop_id == shop_id)
        )
        return result.scalars().all()

    async def get_services(self, shop_id: int):
        result = await self.session.execute(
            select(Service).where(Service.shop_id == shop_id)
        )
        return result.scalars().all()

    async def create_order(self, shop_id: int, client_id: int, total_price: int):
        order = Order(shop_id=shop_id, client_id=client_id, total_price=total_price)
        self.session.add(order)
        await self.session.flush()  # получаем id без коммита
        return order

    async def add_order_items(self, order_id: int, items: list, item_type: str):
        for item_obj, qty in items:
            new_item = OrderItem(
                order_id=order_id,
                quantity=qty,
                product_id=item_obj.id if item_type == 'products' else None,
                service_id=item_obj.id if item_type == 'services' else None
            )
            self.session.add(new_item)
        await self.session.commit()

    async def get_order_with_items(self, order_id: int):
        result = await self.session.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.items).selectinload(OrderItem.service)
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_images_for_product(self, product_id: int, base_path: str):
        imgs = await self.session.execute(
            select(ProductImage).where(ProductImage.product_id == product_id)
        )
        result = [str(Path(base_path) / img.image_url) for img in imgs.scalars().all() if img.image_url]
        return result

    async def generate_comment(self, order_id: int) -> str:
        order = await self.get_order_with_items(order_id)
        if not order:
            return ""
        comment = f"Заказ #{order.id}\nСостав:\n"
        for item in order.items:
            if item.product:
                comment += f"- {item.product.name} x {item.quantity}\n"
            elif item.service:
                comment += f"- {item.service.name} x {item.quantity}\n"
        return comment

    async def create_courier_order(self, client_id: int, shop: Shop, point_b: tuple,
                                   comment: str, price: float, distance: float):
        courier_order = CourierOrder(
            client_id=client_id,
            point_a_lat=shop.point_a_lat,
            point_a_lng=shop.point_a_lng,
            point_b_lat=point_b[0],
            point_b_lng=point_b[1],
            comment=comment,
            status='new',
            price=price,
            distance_km=distance
        )
        self.session.add(courier_order)
        await self.session.commit()
        return courier_order