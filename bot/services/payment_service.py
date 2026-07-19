from datetime import datetime
from decimal import Decimal

from sqlalchemy import select, func

from bot.database.models import Payment
from bot.services.base import BaseService


class PaymentService(BaseService):
    """Запись ПОДТВЕРЖДЁННЫХ пополнений (таблица payments_payment)."""

    async def transaction_exists(self, transaction_id: str) -> bool:
        """Защита от повторной отправки одного и того же чека."""
        if not transaction_id:
            return False
        result = await self.session.execute(
            select(func.count(Payment.id)).where(
                Payment.transaction_id == transaction_id
            )
        )
        return (result.scalar() or 0) > 0

    async def record_payment(
        self,
        *,
        client_id: int | None,
        tg_code: str,
        username: str,
        amount: Decimal,
        method: str,  # 'ocr' | 'admin'
        transaction_id: str = '',
        ocr_confidence: float | None = None,
        receipt_datetime: datetime | None = None,
    ) -> Payment:
        payment = Payment(
            client_id=client_id,
            tg_code=str(tg_code),
            username=username or '',
            amount=Decimal(str(amount)),
            method=method,
            transaction_id=transaction_id or '',
            ocr_confidence=ocr_confidence,
            receipt_datetime=receipt_datetime,
        )
        self.session.add(payment)
        await self.session.commit()
        return payment
