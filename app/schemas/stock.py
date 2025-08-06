from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class StockSaleOut(BaseModel):
    id: UUID
    stock_package_id: UUID
    customer_name: str
    cells_sold: int
    sale_date: date

    model_config = ConfigDict(from_attributes=True)

class StockSaleCreate(BaseModel):
    stock_package_id: UUID
    customer_name: str
    cells_sold: int
