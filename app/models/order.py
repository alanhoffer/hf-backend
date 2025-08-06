from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class CustomerOrder(Base):
    __tablename__ = "customer_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customer_name = Column(String(255), nullable=False)
    number_of_cells = Column(Integer, nullable=False)
    delivery_date = Column(Date, nullable=False)
    larvae_transfer_date = Column(Date, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)