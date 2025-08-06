from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, date
from app.core.database import SessionLocal
from app.models.production import ProductionRecord
from app.schemas.production import ProductionCreate, ProductionOut, ProductionAcceptanceUpdate
from app.routers.auth import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[ProductionOut])
def get_productions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ProductionRecord).filter(ProductionRecord.user_id == current_user.id).all()


@router.post("/", response_model=ProductionOut)
def create_production(prod: ProductionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_record = ProductionRecord(
        id=uuid4(),
        user_id=current_user.id,
        **prod.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/{production_id}", response_model=ProductionOut)
def get_production(production_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(ProductionRecord).filter(ProductionRecord.id == production_id, ProductionRecord.user_id == current_user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Production record not found")
    return record


@router.put("/{production_id}", response_model=ProductionOut)
def update_production(production_id: UUID, prod: ProductionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(ProductionRecord).filter(ProductionRecord.id == production_id, ProductionRecord.user_id == current_user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Production record not found")

    for key, value in prod.dict().items():
        setattr(record, key, value)
    record.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(record)
    return record


@router.put("/{production_id}/acceptance", response_model=ProductionOut)
def update_acceptance(production_id: UUID, acceptance: ProductionAcceptanceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(ProductionRecord).filter(ProductionRecord.id == production_id, ProductionRecord.user_id == current_user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Production record not found")

    record.accepted_cells = acceptance.accepted_cells
    record.acceptance_date = acceptance.acceptance_date or date.today()
    record.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{production_id}")
def delete_production(production_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(ProductionRecord).filter(ProductionRecord.id == production_id, ProductionRecord.user_id == current_user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Production record not found")
    db.delete(record)
    db.commit()
    return {"detail": "Production record deleted"}
