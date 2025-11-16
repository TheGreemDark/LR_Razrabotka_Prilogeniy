from pydantic import BaseModel, Field
from typing import Optional

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Количество товара больше 0")

class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, description="Количество товара больше 0")
    status: Optional[str] = Field(None, description="Статус заказа")