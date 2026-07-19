from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from sqlalchemy import (
    JSON, String, Integer, Float, Boolean, DateTime, ForeignKey,
    Text, Numeric, Time, BigInteger, Table, Column
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


client_favorites = Table(
    "client_client_favorites",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("client_id", ForeignKey("client_client.id")),
    Column("clientad_id", ForeignKey("client_clientad.id")),
)


class Client(Base):
    __tablename__ = "client_client"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(200))
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    username: Mapped[Optional[str]] = mapped_column(String(150))
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
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

    ads: Mapped[List["ClientAd"]] = relationship(back_populates="client")
    favorites: Mapped[List["ClientAd"]] = relationship(
        secondary=client_favorites,
        back_populates="favorited_by"
    )
    sent_transactions: Mapped[List["TeziksTransaction"]] = relationship(
        foreign_keys="[TeziksTransaction.sender_id]",
        back_populates="sender"
    )
    received_transactions: Mapped[List["TeziksTransaction"]] = relationship(
        foreign_keys="[TeziksTransaction.receiver_id]",
        back_populates="receiver"
    )


class ClientAd(Base):
    __tablename__ = "client_clientad"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client_client.id"))
    category_slug: Mapped[str] = mapped_column(String(100))
    subcategory_slug: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default='')
    status_label: Mapped[str] = mapped_column(String(100), default='')
    show_phone: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(10), default='KGS')
    channel_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(BigInteger)
    full_message_ids: Mapped[List[int]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default='active')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client: Mapped["Client"] = relationship(back_populates="ads")
    favorited_by: Mapped[List["Client"]] = relationship(
        secondary=client_favorites,
        back_populates="favorites"
    )


class TeziksTransaction(Base):
    __tablename__ = "client_tezikstransaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_client.id"))
    receiver_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_client.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sender: Mapped[Optional["Client"]] = relationship(
        foreign_keys=[sender_id],
        back_populates="sent_transactions"
    )
    receiver: Mapped[Optional["Client"]] = relationship(
        foreign_keys=[receiver_id],
        back_populates="received_transactions"
    )


class Payment(Base):
    __tablename__ = "payments_payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(ForeignKey("client_client.id"))
    tg_code: Mapped[str] = mapped_column(String(50), default='')
    username: Mapped[str] = mapped_column(String(150), default='')
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    method: Mapped[str] = mapped_column(String(10))  # 'ocr' | 'admin'
    transaction_id: Mapped[str] = mapped_column(String(100), default='')
    ocr_confidence: Mapped[Optional[float]] = mapped_column(Float)
    receipt_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FAQCategory(Base):
    __tablename__ = "faq_faqcategory"

    id: Mapped[int] = mapped_column(primary_key=True)
    app_type: Mapped[str] = mapped_column(String(30), default='market_bot')
    name: Mapped[str] = mapped_column(String(100))
    name_en: Mapped[str] = mapped_column(String(100), default='')
    name_kg: Mapped[str] = mapped_column(String(100), default='')
    name_cn: Mapped[str] = mapped_column(String(100), default='')
    emoji: Mapped[str] = mapped_column(String(8), default='')
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[List["FAQItem"]] = relationship(back_populates="category")


class FAQItem(Base):
    __tablename__ = "faq_faqitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("faq_faqcategory.id"))
    question: Mapped[str] = mapped_column(String(255))
    question_en: Mapped[str] = mapped_column(String(255), default='')
    question_kg: Mapped[str] = mapped_column(String(255), default='')
    question_cn: Mapped[str] = mapped_column(String(255), default='')
    answer: Mapped[str] = mapped_column(Text)
    answer_en: Mapped[str] = mapped_column(Text, default='')
    answer_kg: Mapped[str] = mapped_column(Text, default='')
    answer_cn: Mapped[str] = mapped_column(Text, default='')
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category: Mapped["FAQCategory"] = relationship(back_populates="items")