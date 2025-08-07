from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

class HiveOut(BaseModel):
    hive_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductionOut(BaseModel):
    id: UUID
    user_id: UUID
    order_id: Optional[str] = None
    transfer_date: date
    acceptance_date: Optional[date] = None
    cells_produced: int
    larvae_transferred: int
    notes: Optional[str] = None
    created_at: datetime
    hives: List[HiveOut] = []  # <--- aquí aseguramos que venga lista, no None

    model_config = ConfigDict(from_attributes=True)

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


class ProductionAcceptanceUpdate(BaseModel):
    accepted_cells: int
    acceptance_date: Optional[date] = None

