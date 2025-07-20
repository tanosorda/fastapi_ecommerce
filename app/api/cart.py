from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, database
from ..dependencies import get_current_user_id

router = APIRouter(tags=["cart"])

@router.get("/cart/", response_model=schemas.Cart)
async def get_user_cart(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(database.get_db)
):
    cart = await crud.get_cart_by_user(db, user_id=user_id)
    if not cart:
        cart = await crud.create_cart(db, schemas.CartBase(user_id=user_id))
    return cart

@router.post("/cart/items/", response_model=schemas.CartItem)
async def add_item_to_cart(
    item: schemas.CartItemCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(database.get_db)
):
    cart = await crud.get_cart_by_user(db, user_id=user_id)
    if not cart:
        cart = await crud.create_cart(db, schemas.CartBase(user_id=user_id))
    return await crud.add_cart_item(db, cart_id=cart.id, item=item)

@router.put("/cart/items/{item_id}", response_model=schemas.CartItem)
async def update_cart_item_quantity(
    item_id: int,
    quantity: int,
    db: AsyncSession = Depends(database.get_db)
):
    updated_item = await crud.update_cart_item_quantity(db, item_id=item_id, quantity=quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item

@router.delete("/cart/items/{item_id}")
async def remove_cart_item(
    item_id: int,
    db: AsyncSession = Depends(database.get_db)
):
    await crud.remove_cart_item(db, item_id=item_id)
    return {"message": "Item removed from cart"}