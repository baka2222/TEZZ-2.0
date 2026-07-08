from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, ForeignKey, 
    Text, Numeric, Time, BigInteger
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "client_client"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(200))
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    username: Mapped[Optional[str]] = mapped_column(String(150))
    language: Mapped[str] = mapped_column(String(2), default='ru')
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    next_subscription_disable: Mapped[Optional[datetime]] = mapped_column(DateTime)
    next_ability: Mapped[Optional[datetime]] = mapped_column(DateTime)
    next_ability_beauty: Mapped[Optional[datetime]] = mapped_column(DateTime)
    next_ability_automoto: Mapped[Optional[datetime]] = mapped_column(DateTime)
    next_ability_housing: Mapped[Optional[datetime]] = mapped_column(DateTime)
    next_ability_techno: Mapped[Optional[datetime]] = mapped_column(DateTime)
    next_ability_job: Mapped[Optional[datetime]] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shops: Mapped[List["Shop"]] = relationship(back_populates="owner")
    orders: Mapped[List["Order"]] = relationship(back_populates="client")
    delivery_orders: Mapped[List["CourierOrder"]] = relationship(
        foreign_keys="[CourierOrder.client_id]",
        back_populates="client"
    )
    assigned_deliveries: Mapped[List["CourierOrder"]] = relationship(
        foreign_keys="[CourierOrder.courier_id]",
        back_populates="courier"
    )


class Category(Base):
    __tablename__ = "client_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    name_en: Mapped[str] = mapped_column(String(100))
    name_kg: Mapped[str] = mapped_column(String(100))
    name_cn: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)

    shops: Mapped[List["Shop"]] = relationship(back_populates="category")


class Shop(Base):
    __tablename__ = "client_shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("client_client.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_category.id"))
    
    point_a_lat: Mapped[float] = mapped_column(Float)
    point_a_lng: Mapped[float] = mapped_column(Float)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[Optional[str]] = mapped_column(String(300))
    description: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    description_kg: Mapped[Optional[str]] = mapped_column(Text)
    description_cn: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped["Client"] = relationship(back_populates="shops")
    category: Mapped[Optional["Category"]] = relationship(back_populates="shops")
    products: Mapped[List["Product"]] = relationship(back_populates="shop")
    services: Mapped[List["Service"]] = relationship(back_populates="shop")
    orders: Mapped[List["Order"]] = relationship(back_populates="shop")


class Product(Base):
    __tablename__ = "client_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("client_shop.id"))
    name: Mapped[str] = mapped_column(String(200))
    name_en: Mapped[Optional[str]] = mapped_column(String(200))
    name_kg: Mapped[Optional[str]] = mapped_column(String(200))
    name_cn: Mapped[Optional[str]] = mapped_column(String(200))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    description_kg: Mapped[Optional[str]] = mapped_column(Text)
    description_cn: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    shop: Mapped["Shop"] = relationship(back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
    images: Mapped[List["ProductImage"]] = relationship(back_populates="product")


class ProductImage(Base):
    __tablename__ = "client_productimage"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("client_product.id"))
    image_url: Mapped[str] = mapped_column(String(500))

    product: Mapped["Product"] = relationship(back_populates="images")


class Service(Base):
    __tablename__ = "client_service"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("client_shop.id"))
    name: Mapped[str] = mapped_column(String(200))
    name_en: Mapped[Optional[str]] = mapped_column(String(200))
    name_kg: Mapped[Optional[str]] = mapped_column(String(200))
    name_cn: Mapped[Optional[str]] = mapped_column(String(200))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    description_en: Mapped[Optional[str]] = mapped_column(Text)
    description_kg: Mapped[Optional[str]] = mapped_column(Text)
    description_cn: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    shop: Mapped["Shop"] = relationship(back_populates="services")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="service")


class Order(Base):
    __tablename__ = "client_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("client_shop.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("client_client.id"))
    total_price: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    shop: Mapped["Shop"] = relationship(back_populates="orders")
    client: Mapped["Client"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "client_orderitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("client_order.id"))
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_product.id"), nullable=True)
    service_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_service.id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped[Optional["Product"]] = relationship(back_populates="order_items")
    service: Mapped[Optional["Service"]] = relationship(back_populates="order_items")


class PricingRule(Base):
    __tablename__ = "client_pricingrule"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    min_distance: Mapped[float] = mapped_column(Float, default=0)
    max_distance: Mapped[float] = mapped_column(Float, default=0)
    base_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=0)
    per_km_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=0)
    multiplier: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=1)


class TimeSurcharge(Base):
    __tablename__ = "client_timesurcharge"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    multiplier: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=1)


class CourierOrder(Base):
    __tablename__ = "client_courierorder"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client_client.id"))
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_client.id"))
    
    point_a_lat: Mapped[float] = mapped_column(Float)
    point_a_lng: Mapped[float] = mapped_column(Float)
    point_b_lat: Mapped[float] = mapped_column(Float)
    point_b_lng: Mapped[float] = mapped_column(Float)
    
    status: Mapped[str] = mapped_column(String(20), default='new')
    comment: Mapped[Optional[str]] = mapped_column(Text)
    distance_km: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client: Mapped["Client"] = relationship(
        foreign_keys=[client_id],
        back_populates="delivery_orders"
    )
    courier: Mapped[Optional["Client"]] = relationship(
        foreign_keys=[courier_id],
        back_populates="assigned_deliveries"
    )