# app/schemas/dashboard.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from uuid import UUID

class StatsOut(BaseModel):
    total_available_cells: int
    pending_orders: int
    expiring_stock: int
    total_sales_last_30_days: int

class UpcomingItem(BaseModel):
    id: UUID
    customer_name: str
    delivery_date: date
    larvae_transfer_date: date
    number_of_cells: int

class ExpiringItem(BaseModel):
    id: UUID
    production_date: date
    available_cells: int
    expiration_date: date