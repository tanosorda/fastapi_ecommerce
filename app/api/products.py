from fastapi import APIRouter, HTTPException
from db.repository import ProductRepository
from schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    return await ProductRepository.create(product.model_dump())

@router.get("/", response_model=list[ProductResponse])
async def get_products():
    return await ProductRepository.get_all()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    product = await ProductRepository.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate):
    updated = await ProductRepository.update(product_id, product.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    success = await ProductRepository.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}