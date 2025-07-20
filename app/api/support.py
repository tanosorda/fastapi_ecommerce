from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, database
from ..dependencies import get_current_user_id
from typing import List

router = APIRouter(tags=["support"])

@router.post("/support/", response_model=schemas.SupportTicket)
async def create_support_ticket(
    ticket: schemas.SupportTicketCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_support_ticket(db, ticket=ticket, user_id=user_id)

@router.get("/support/", response_model=List[schemas.SupportTicket])
async def get_user_support_tickets(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.get_support_tickets(db, user_id=user_id)

@router.get("/support/{ticket_id}", response_model=schemas.SupportTicket)
async def get_support_ticket(
    ticket_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(database.get_db)
):
    ticket = await crud.get_support_ticket(db, ticket_id=ticket_id, user_id=user_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/support/{ticket_id}/answer", response_model=schemas.SupportTicket)
async def answer_support_ticket(
    ticket_id: int,
    answer: str,
    db: AsyncSession = Depends(database.get_db)
):
    ticket = await crud.answer_support_ticket(db, ticket_id=ticket_id, answer=answer)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket