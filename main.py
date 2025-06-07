
from fastapi import FastAPI
import crud 
import database
from schemas import ItemCreate, ItemUpdate

app = FastAPI(title="Inventory Manager API")

@app.get("/")
async def root():
    return {"message": "Inventory Manager API is running. Visit /docs for API UI."}


@app.on_event("startup")
async def startup():
    await database.init_db()

@app.post("/items/")
async def create_item(item: ItemCreate):
    return await crud.create_item(item)

@app.get("/items/")
async def get_items():
    return await crud.get_all_items()

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    return await crud.get_item(item_id)

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: ItemUpdate):
    return await crud.update_item(item_id, item)

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    return await crud.delete_item(item_id)
