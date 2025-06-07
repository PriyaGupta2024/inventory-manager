
import database
from schemas import ItemCreate, ItemUpdate
from fastapi import HTTPException

async def create_item(item: ItemCreate):
    return await database.insert_item(item)

async def get_item(item_id: str):
    try:
        return await database.fetch_item(item_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")

async def get_all_items():
    return await database.fetch_all_items()

async def update_item(item_id: str, item: ItemUpdate):
    try:
        return await database.update_item(item_id, item)
    except Exception:
        return {"error": "Update failed or item not found"}

async def delete_item(item_id: str):
    try:
        return await database.delete_item(item_id)
    except Exception:
        return {"error": "Delete failed or item not found"}
