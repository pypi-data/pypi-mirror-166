from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    """The format used by the server logic."""

    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class UserItem(BaseModel):
    """The format for creating a new item by the user."""

    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class PatchedUserItem(BaseModel):
    """The format for patching an existing item."""

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None
