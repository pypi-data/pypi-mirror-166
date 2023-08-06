import uvicorn

from os import getenv
from .app import app
from .dummy_data import DummyItemsGenerator
from .exceptions import ItemNotFoundException
from .models.items import Item, PatchedUserItem, UserItem

"""Dummy data"""
dummy_items_gen = DummyItemsGenerator(num_items=100)
items = dummy_items_gen.create_items()


"""Helper functions"""


def check_if_item_exists(id: int) -> bool:
    ids = [item.id for item in items]
    return True if id in ids else False


def check_if_new_id_valid(id: int):
    return id == len(items)


"""HTTP methods"""


@app.get("/", response_model=dict)
async def root():
    """Returns a basic hello message."""
    return {"message": "Hello, ASH!"}


@app.get("/items/", response_model=list[Item])
async def get_items():
    """Returns all items."""
    return items


@app.post("/items/", response_model=Item)
async def post_item(user_item: UserItem):
    """Allows user to add an `Item` to the items list."""
    new_id = len(items)
    new_item = Item(id=new_id, **user_item.dict())
    items.append(new_item)

    return new_item


@app.get("/items/{id}", response_model=Item)
async def get_item(id: int):
    """Returns an `Item` based on `ID`, if `ID` is valid and exists; else, raises `ItemNotFoundException`."""
    if check_if_item_exists(id) == False:
        raise ItemNotFoundException(id)

    return items[id]


@app.patch("/items/{id}", response_model=Item)
async def patch_item(id: int, patches: PatchedUserItem):
    """Allows user to patch item, if `ID` is valid and exists; else, raises `ItemNotFoundException`."""
    if check_if_item_exists(id) == False:
        raise ItemNotFoundException(id)

    stored_item = items[id]
    updated_item = stored_item.copy(update=patches.dict(exclude_unset=True))
    items[id] = updated_item

    return updated_item


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
