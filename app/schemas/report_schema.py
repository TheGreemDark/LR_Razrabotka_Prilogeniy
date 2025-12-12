from datetime import date

from pydantic import BaseModel


class OrderReportRead(BaseModel):
    id: int
    report_at: date
    order_id: int
    count_product: int

    class Config:
        from_attributes = True  # для Litestar + SQLAlchemy
