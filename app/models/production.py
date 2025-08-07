from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class ProductionRecord(Base):
    __tablename__ = "production_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transfer_date = Column(Date, nullable=False)
    larvae_transferred = Column(Integer, nullable=False)
    accepted_cells = Column(Integer)
    acceptance_date = Column(Date)
    cells_produced = Column(Integer, nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("customer_orders.id", ondelete="SET NULL"))
    notes = Column(Text)
    status = Column(String(50), default="active")
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # 👇 Relación con colmenas asociadas a esta producción
    hives = relationship("Hive", back_populates="production", cascade="all, delete-orphan")



class ProductionHive(Base):
    __tablename__ = "production_hives"

    id = Column(String(36), primary_key=True)
    production_id = Column(String(36), ForeignKey("productions.id"))
    hive_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Hive(Base):
    __tablename__ = "hives"

    id = Column(String(36), primary_key=True, index=True)
    production_id = Column(UUID(as_uuid=True), ForeignKey("production_records.id", ondelete="CASCADE"))
    hive_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # 👇 Relación inversa a la producción
    production = relationship("ProductionRecord", back_populates="hives")