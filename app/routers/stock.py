from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from app.core.database import SessionLocal
from app.models.stock import StockPackage, StockSale
from app.schemas.stock import StockCreate, StockOut, StockSaleCreate, StockSaleOut
from app.routers.auth import get_current_user, get_db

from app.models.user import User
from fastapi import status

router = APIRouter()

@router.get("/", response_model=list[StockOut])
def get_available_stock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(StockPackage).filter(StockPackage.user_id == current_user.id, StockPackage.available_cells > 0, StockPackage.is_expired == False).all()


@router.get("/all", response_model=list[StockOut])
def get_all_stock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(StockPackage).filter(StockPackage.user_id == current_user.id).all()


@router.post("/", response_model=StockOut)
def create_stock_package(stock: StockCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_package = StockPackage(
        id=uuid4(),
        user_id=current_user.id,
        **stock.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    return new_package


@router.post("/{stock_id}/sell", response_model=StockOut, status_code=status.HTTP_201_CREATED)
def sell_cells_from_stock(
    stock_id: UUID,
    sale_data: StockSaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Buscar el paquete de stock
    stock_package = db.query(StockPackage).filter(
        StockPackage.id == stock_id,
        StockPackage.user_id == current_user.id
    ).first()

    if not stock_package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete de stock no encontrado."
        )

    # 2. Validar que hay suficientes celdas disponibles
    if sale_data.cells_sold <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de celdas vendidas debe ser mayor a 0."
        )

    if stock_package.available_cells < sale_data.cells_sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Celdas insuficientes en el paquete. Disponibles: {stock_package.available_cells}"
        )
    
    # 3. Registrar la venta en la tabla stock_sales
    new_sale = StockSale(
        stock_package_id=stock_package.id,
        customer_name=sale_data.customer_name,
        cells_sold=sale_data.cells_sold,
        sale_date=date.today()
    )
    db.add(new_sale)

    # 4. Actualizar el paquete de stock (available_cells, sold_cells)
    stock_package.available_cells -= sale_data.cells_sold
    stock_package.sold_cells += sale_data.cells_sold

    # 5. Si no quedan celdas, actualizar el estado
    if stock_package.available_cells == 0:
        stock_package.is_expired = True

    db.commit()
    db.refresh(stock_package)
    return stock_package

@router.get("/{stock_id}/sales", response_model=list[StockSaleOut])
def get_sales_history_for_package(
    stock_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verificar si el paquete de stock existe y pertenece al usuario
    stock_package = db.query(StockPackage).filter(
        StockPackage.id == stock_id,
        StockPackage.user_id == current_user.id
    ).first()

    if not stock_package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete de stock no encontrado."
        )

    # 2. Buscar las ventas asociadas
    sales_history = db.query(StockSale).filter(
        StockSale.stock_package_id == stock_id
    ).all()
    
    return sales_history