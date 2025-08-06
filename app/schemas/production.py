from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class ProductionBase(BaseModel):
    transfer_date: date
    larvae_transferred: int
    accepted_cells: Optional[int] = None
    acceptance_date: Optional[date] = None
    cells_produced: int
    order_id: Optional[UUID] = None
    notes: Optional[str] = None
    status: str = "active"

class ProductionCreate(ProductionBase):
    pass

class ProductionOut(ProductionBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductionAcceptanceUpdate(BaseModel):
    accepted_cells: int
    acceptance_date: Optional[date] = None
