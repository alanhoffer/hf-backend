from sqlalchemy import Column, Integer, Date, Boolean, TIMESTAMP, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.types import TypeDecorator
import uuid
from app.core.database import Base

# UUID compatible con MySQL (usa CHAR(36))
class GUID(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True  # <--- agregá esta línea

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        elif isinstance(value, uuid.UUID):
            return str(value)
        return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(value)

# ---------- MODELOS ----------

class StockPackage(Base):
    __tablename__ = "stock_packages"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    production_id = Column(GUID(), ForeignKey("production_records.id", ondelete="CASCADE"), nullable=False)
    production_date = Column(Date, nullable=False)
    total_cells = Column(Integer, nullable=False)
    available_cells = Column(Integer, nullable=False)
    sold_cells = Column(Integer, default=0)
    expiration_date = Column(Date, nullable=False)
    is_expired = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    # Relación con ventas
    sales = relationship("StockSale", back_populates="stock_package", cascade="all, delete-orphan")


class StockSale(Base):
    __tablename__ = "stock_sales"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    stock_package_id = Column(GUID(), ForeignKey("stock_packages.id", ondelete="CASCADE"))
    customer_name = Column(String(255), nullable=False)
    cells_sold = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stock_package = relationship("StockPackage", back_populates="sales")
