from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.repositories import repository
from app.schemas import schemas
from app.db.database import get_db
from app.dependencies import get_current_user_id

router = APIRouter(tags=["support"])

@router.post("/support/", response_model=schemas.SupportTicket)
async def create_support_ticket(
    ticket: schemas.SupportTicketCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await repository.create_support_ticket(db, ticket=ticket, user_id=user_id)

@router.get("/support/", response_model=List[schemas.SupportTicket])
async def get_user_support_tickets(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await repository.get_support_tickets(db, user_id=user_id)

@router.get("/support/{ticket_id}", response_model=schemas.SupportTicket)
async def get_support_ticket(
    ticket_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    ticket = await repository.get_support_ticket(db, ticket_id=ticket_id, user_id=user_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/support/{ticket_id}/answer", response_model=schemas.SupportTicket)
async def answer_support_ticket(
    ticket_id: int,
    answer: str,  # здесь можно заменить на Pydantic-модель, если нужно
    db: AsyncSession = Depends(get_db)
):
    ticket = await repository.answer_support_ticket(db, ticket_id=ticket_id, answer=answer)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
