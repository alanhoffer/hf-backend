from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
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
