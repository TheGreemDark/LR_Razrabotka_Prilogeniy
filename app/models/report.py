from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.user import Base


class OrderReport(Base):
    __tablename__ = "order_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_at: Mapped[date] = mapped_column(Date, nullable=False)  # день отчёта
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    count_product: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # количество товаров в заказе
