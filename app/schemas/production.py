from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime
from typing import List, Optional


class HiveOut(BaseModel):
    hive_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class ProductionOut(BaseModel):
    id: str
    order_id: str
    transfer_date: date
    acceptance_date: date | None
    cells_produced: int
    larvae_transferred: int
    notes: str
    created_at: datetime
    hives: List[HiveOut]  # ✅ Hives incluidos

    class Config:
        orm_mode = True
        
class HiveCreate(BaseModel):
    hive_name: str
class ProductionBase(BaseModel):
    transfer_date: date
    larvae_transferred: int
    accepted_cells: Optional[int] = None
    acceptance_date: Optional[date] = None
    cells_produced: int
    order_id: Optional[UUID] = None
    notes: Optional[str] = None
    status: str = "active"

class ProductionCreate(BaseModel):
    transfer_date: date
    larvae_transferred: int
    accepted_cells: Optional[int] = None
    acceptance_date: Optional[date] = None
    cells_produced: int
    order_id: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = "active"
    hives: List[HiveCreate]

class ProductionOut(ProductionBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductionAcceptanceUpdate(BaseModel):
    accepted_cells: int
    acceptance_date: Optional[date] = None

