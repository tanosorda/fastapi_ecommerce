from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.repositories import repository
from app.schemas import schemas
from app.db.database import get_db

router = APIRouter(tags=["categories"])

@router.post("/categories/", response_model=schemas.Category)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    return await repository.create_category(db, category=category)

@router.get("/categories/", response_model=List[schemas.CategoryWithChildren])
async def read_root_categories(db: AsyncSession = Depends(get_db)):
    return await repository.get_root_categories(db)

@router.get("/categories/{category_id}", response_model=schemas.CategoryWithChildren)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await repository.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/{category_id}/products", response_model=List[schemas.Product])
async def read_category_products(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await repository.get_products_by_category(db, category_id)
