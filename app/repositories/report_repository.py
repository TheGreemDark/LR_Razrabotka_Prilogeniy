from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderReport


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_date(self, report_at: date) -> list[OrderReport]:
        stmt = select(OrderReport).where(OrderReport.report_at == report_at)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
