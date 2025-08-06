from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

class StockBase(BaseModel):
    production_id: UUID
    production_date: date
    total_cells: int
    available_cells: int
    sold_cells: int = 0
    expiration_date: date
    is_expired: bool = False

class StockCreate(StockBase):
    pass

class StockOut(StockBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True  # usa from_attributes en lugar de orm_mode

class StockSaleOut(BaseModel):
    id: UUID
    stock_package_id: UUID
    customer_name: str
    cells_sold: int
    sale_date: date

    class Config:
        from_attributes = True

class StockSaleCreate(BaseModel):
    stock_package_id: UUID   # faltaba esto
    customer_name: str
    cells_sold: int
