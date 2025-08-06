# app/routers/reports.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import SessionLocal
from app.routers.auth import get_current_user, get_db
from app.models.user import User
from app.models.order import CustomerOrder
from app.models.production import ProductionRecord
from app.schemas.order import OrderOut
from app.schemas.production import ProductionOut
from app.schemas.reports import ReportQueryParams
from app.schemas.reports import ReportType

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from typing import Optional

import io
import csv
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/orders", response_model=List[OrderOut])
def get_order_history(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None, description="Filtrar pedidos desde esta fecha"),
    end_date: Optional[date] = Query(None, description="Filtrar pedidos hasta esta fecha"),
    status: Optional[str] = Query(None, description="Filtrar por estado (e.g., 'pending', 'delivered')"),
    customer_name: Optional[str] = Query(None, description="Filtrar por nombre del cliente")
):
    """
    Obtiene el historial de pedidos de clientes con filtros opcionales.
    """
    query = db.query(CustomerOrder).filter(CustomerOrder.user_id == current_user.id)

    if start_date:
        query = query.filter(CustomerOrder.created_at >= start_date)
    if end_date:
        query = query.filter(CustomerOrder.created_at <= end_date)
    if status:
        query = query.filter(CustomerOrder.status == status)
    if customer_name:
        query = query.filter(CustomerOrder.customer_name.ilike(f"%{customer_name}%"))

    return query.all()

@router.get("/productions", response_model=List[ProductionOut])
def get_production_history(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None, description="Filtrar producciones desde esta fecha"),
    end_date: Optional[date] = Query(None, description="Filtrar producciones hasta esta fecha"),
    status: Optional[str] = Query(None, description="Filtrar por estado (e.g., 'active', 'expired')")
):
    """
    Obtiene el historial de registros de producción con filtros opcionales.
    """
    query = db.query(ProductionRecord).filter(ProductionRecord.user_id == current_user.id)

    if start_date:
        query = query.filter(ProductionRecord.created_at >= start_date)
    if end_date:
        query = query.filter(ProductionRecord.created_at <= end_date)
    if status:
        query = query.filter(ProductionRecord.status == status)

    return query.all()


@router.get("/export/csv", response_model=None)
def export_data_to_csv(
    report_type: ReportType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    """
    Exporta datos de órdenes o producciones a un archivo CSV.
    """
    if report_type == ReportType.orders:
        records = get_order_history(db, current_user, start_date=start_date, end_date=end_date)
        if not records:
            raise HTTPException(status_code=404, detail="No hay datos para exportar")
        
        # Preparamos los datos
        header = ["ID", "Customer Name", "Number of Cells", "Delivery Date", "Status"]
        data = [[str(r.id), r.customer_name, r.number_of_cells, r.delivery_date, r.status] for r in records]
        filename = "orders_report.csv"
    
    elif report_type == ReportType.productions:
        records = get_production_history(db, current_user, start_date=start_date, end_date=end_date)
        if not records:
            raise HTTPException(status_code=404, detail="No hay datos para exportar")
        
        # Preparamos los datos
        header = ["ID", "Transfer Date", "Larvae Transferred", "Accepted Cells", "Cells Produced", "Status"]
        data = [[str(r.id), r.transfer_date, r.larvae_transferred, r.accepted_cells, r.cells_produced, r.status] for r in records]
        filename = "productions_report.csv"
    
    else:
        raise HTTPException(status_code=400, detail="Tipo de reporte no válido")

    # Escribimos los datos en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(header)
    writer.writerows(data)
    
    # Preparamos la respuesta de streaming
    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

@router.get("/export/pdf", response_model=None)
def export_data_to_pdf(
    report_type: ReportType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    """
    Exporta datos de órdenes o producciones a un archivo PDF.
    """
    if report_type == ReportType.orders:
        records = get_order_history(db, current_user, start_date=start_date, end_date=end_date)
        if not records:
            raise HTTPException(status_code=404, detail="No hay datos para exportar")
        
        header = ["ID", "Nombre Cliente", "Celdas", "Fecha de Entrega", "Estado"]
        data = [header] + [[str(r.id)[:8] + '...', r.customer_name, str(r.number_of_cells), str(r.delivery_date), r.status] for r in records]
        filename = "orders_report.pdf"
    
    elif report_type == ReportType.productions:
        records = get_production_history(db, current_user, start_date=start_date, end_date=end_date)
        if not records:
            raise HTTPException(status_code=404, detail="No hay datos para exportar")
        
        header = ["ID", "Fecha de Transferencia", "Larvas", "Aceptadas", "Producidas", "Estado"]
        data = [header] + [[str(r.id)[:8] + '...', str(r.transfer_date), str(r.larvae_transferred), str(r.accepted_cells), str(r.cells_produced), r.status] for r in records]
        filename = "productions_report.pdf"

    else:
        raise HTTPException(status_code=400, detail="Tipo de reporte no válido")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})