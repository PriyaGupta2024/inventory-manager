"""
it is for me  better understanding  
schemas.py – Pydantic models :- This model means:

You expect data with three fields: name (string), email (string), and age (integer).

FastAPI will use this to:

Check incoming data (validate it).

Convert it into a Python object.

Generate automatic API docs. """


from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    category: str
    price: float
    in_stock: bool

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None

class Item(ItemBase):
    id: str
