from datetime import date

from litestar import Controller, get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderReport


class ReportController(Controller):
    path = "/report"

    @get(path="")
    async def get_report(
        self,
        report_at: date,
        db_session: AsyncSession,
    ) -> list[dict]:
        print("GET /report called, report_at =", report_at)

        stmt = select(OrderReport).where(OrderReport.report_at == report_at)
        result = await db_session.execute(stmt)
        rows = result.scalars().all()

        # отладочный вывод, чтобы убедиться, что именно приходит
        print("rows =", rows)

        response: list[dict] = []
        for r in rows:
            response.append(
                {
                    "id": r.id,
                    "report_at": r.report_at.isoformat() if r.report_at else None,
                    "order_id": r.order_id,
                    "count_product": r.count_product,
                }
            )

        return response
