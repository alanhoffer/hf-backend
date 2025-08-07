from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class ProductionRecord(Base):
    __tablename__ = "production_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transfer_date = Column(Date, nullable=False)
    larvae_transferred = Column(Integer, nullable=False)
    accepted_cells = Column(Integer)
    acceptance_date = Column(Date)
    cells_produced = Column(Integer, nullable=False)
    order_id = Column(String(36), ForeignKey("customer_orders.id", ondelete="SET NULL"))
    notes = Column(Text)
    status = Column(String(50), default="active")
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    hives = relationship("Hive", back_populates="production", cascade="all, delete-orphan")


class Hive(Base):
    __tablename__ = "hives"

    id = Column(String(36), primary_key=True, index=True, default=generate_uuid)
    production_id = Column(String(36), ForeignKey("production_records.id", ondelete="CASCADE"))
    hive_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    production = relationship("ProductionRecord", back_populates="hives")


class ProductionHive(Base):
    __tablename__ = "production_hives"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    production_id = Column(String(36), ForeignKey("production_records.id", ondelete="CASCADE"))
    hive_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
