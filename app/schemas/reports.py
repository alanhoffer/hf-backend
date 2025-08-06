# app/schemas/reports.py
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class ReportType(str, Enum):
    orders = "orders"
    productions = "productions"

class ReportQueryParams(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    customer_name: Optional[str] = None