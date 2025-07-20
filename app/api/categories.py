from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/categories/", response_model=schemas.Category)
async def create_category(
    category: schemas.CategoryCreate, 
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_category(db, category=category)

@router.get("/categories/", response_model=List[schemas.CategoryWithChildren])
async def read_root_categories(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_root_categories(db)

@router.get("/categories/{category_id}", response_model=schemas.CategoryWithChildren)
async def read_category(category_id: int, db: AsyncSession = Depends(database.get_db)):
    category = await crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/{category_id}/products", response_model=List[schemas.Product])
async def read_category_products(
    category_id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.get_products_by_category(db, category_id)