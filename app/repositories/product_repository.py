from sqlalchemy.ext.asyncio import AsyncSession
from models import Product
from sqlalchemy import select


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Product]:
        query = select(Product)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, title: str, price_cents: int, quantity_tovar: int) -> Product:
        product = Product(
            title=title,
            price_cents=price_cents,
            quantity_tovar=quantity_tovar
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update_stock(self, product_id: int, new_quantity: int) -> Product | None:
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        product.quantity_tovar = new_quantity
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: int) -> None:
        product = await self.get_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()