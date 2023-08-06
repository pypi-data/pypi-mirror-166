from fastapi import Request
from fastapi.responses import JSONResponse

from .app import app


class ItemNotFoundException(Exception):
    def __init__(self, name):
        self.name = name


@app.exception_handler(ItemNotFoundException)
async def item_not_found_exception_handler(
    request: Request, exc: ItemNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item with ID [{exc.name}] not found or invalid"},
    )


class NewItemIDNotValidException(Exception):
    def __init__(self, name):
        self.name = name


@app.exception_handler(NewItemIDNotValidException)
async def new_item_id_not_valid_exception_handler(
    request: Request, exc: ItemNotFoundException
):
    return JSONResponse(status_code=406, content={"message": f"Invalid item ID."})
