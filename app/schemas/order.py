from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime

class OrderBase(BaseModel):
    customer_name: str
    number_of_cells: int
    delivery_date: date
    larvae_transfer_date: date
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
