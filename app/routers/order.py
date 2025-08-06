from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.order import CustomerOrder
from app.schemas.order import OrderCreate, OrderOut
from app.routers.auth import get_current_user, get_db
from app.models.user import User
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(CustomerOrder).filter(CustomerOrder.user_id == current_user.id).all()


@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_order = CustomerOrder(
        id=uuid4(),
        user_id=current_user.id,
        **order.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(CustomerOrder).filter(CustomerOrder.id == order_id, CustomerOrder.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: UUID, order_update: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(CustomerOrder).filter(CustomerOrder.id == order_id, CustomerOrder.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_update.dict().items():
        setattr(order, key, value)
    order.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}")
def delete_order(order_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(CustomerOrder).filter(CustomerOrder.id == order_id, CustomerOrder.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}
