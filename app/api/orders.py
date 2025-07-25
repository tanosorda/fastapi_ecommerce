from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.repositories import repository
from app.schemas import schemas
from app.db.database import get_db  # импорт get_db
from app.dependencies import get_current_user_id

router = APIRouter() 

@router.post("/orders/", response_model=schemas.Order)
async def create_order(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    order = await repository.create_order(db, user_id=user_id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return order

@router.get("/orders/", response_model=List[schemas.Order])
async def get_user_orders(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await repository.get_orders_by_user(db, user_id=user_id)

@router.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order_details(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    order = await repository.get_order_by_id(db, order_id=order_id, user_id=user_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(
    order_id: int,
    status: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    valid_statuses = ["pending", "awaiting_confirmation", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    order = await repository.update_order_status(db, order_id=order_id, status=status, user_id=user_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
