# app/routers/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.database import SessionLocal
from app.routers.auth import get_current_user, get_db
from app.models.user import User
from app.models.stock import StockPackage, StockSale
from app.models.order import CustomerOrder
from app.schemas.dashboard import StatsOut, UpcomingItem, ExpiringItem
from typing import List
from sqlalchemy import func



router = APIRouter()

@router.get("/stats", response_model=StatsOut)
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtiene estadísticas clave del dashboard para el usuario actual.
    """
    # Total de celdas disponibles
    total_available_cells = db.query(
        func.sum(StockPackage.available_cells)
    ).filter(
        StockPackage.user_id == current_user.id,
        StockPackage.is_expired == False
    ).scalar() or 0

    # Órdenes pendientes
    pending_orders = db.query(CustomerOrder).filter(
        CustomerOrder.user_id == current_user.id,
        CustomerOrder.status == 'pending'
    ).count()

    # Stock por expirar (en los próximos 7 días)
    expiring_date = date.today() + timedelta(days=7)
    expiring_stock = db.query(StockPackage).filter(
        StockPackage.user_id == current_user.id,
        StockPackage.is_expired == False,
        StockPackage.expiration_date <= expiring_date
    ).count()

    # Ventas en los últimos 30 días
    last_30_days = date.today() - timedelta(days=30)
    sales_last_30_days = db.query(
        func.sum(StockSale.cells_sold)
    ).join(
        StockPackage, StockPackage.id == StockSale.stock_package_id
    ).filter(
        StockPackage.user_id == current_user.id,
        StockSale.sale_date >= last_30_days
    ).scalar() or 0

    return StatsOut(
        total_available_cells=total_available_cells,
        pending_orders=pending_orders,
        expiring_stock=expiring_stock,
        total_sales_last_30_days=sales_last_30_days
    )

@router.get("/upcoming", response_model=List[UpcomingItem])
def get_upcoming_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtiene los próximos pedidos de clientes que se deben preparar.
    """
    upcoming_orders = db.query(CustomerOrder).filter(
        CustomerOrder.user_id == current_user.id,
        CustomerOrder.status.in_(['pending', 'in_production']),
        CustomerOrder.larvae_transfer_date >= date.today()
    ).order_by(CustomerOrder.larvae_transfer_date).limit(10).all()

    return [
        UpcomingItem(
            id=order.id,
            customer_name=order.customer_name,
            delivery_date=order.delivery_date,
            larvae_transfer_date=order.larvae_transfer_date,
            number_of_cells=order.number_of_cells
        )
        for order in upcoming_orders
    ]


@router.get("/expiring", response_model=List[ExpiringItem])
def get_expiring_stock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtiene los paquetes de stock que están cerca de expirar.
    """
    expiring_date = date.today() + timedelta(days=7)
    expiring_stock = db.query(StockPackage).filter(
        StockPackage.user_id == current_user.id,
        StockPackage.is_expired == False,
        StockPackage.available_cells > 0,
        StockPackage.expiration_date <= expiring_date
    ).order_by(StockPackage.expiration_date).all()
    
    return expiring_stock