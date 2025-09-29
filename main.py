"""
Simple FastAPI application for IIS test
======================================

This FastAPI app defines a couple of basic endpoints so you can verify that
FastAPI works correctly when hosted behind Microsoft Internet Information
Services (IIS) using the HttpPlatformHandler module.  The root endpoint
returns a greeting, and there is a second endpoint that accepts a path
parameter and an optional query string parameter.  These endpoints are kept
simple on purpose—once you have them working through IIS you can expand
the application as needed.
"""

from fastapi import FastAPI
from typing import Union

# Create the FastAPI application instance
app = FastAPI(title="IIS FastAPI Test",
              description="Basic FastAPI app served by IIS via HttpPlatformHandler",
              version="0.1.0")


@app.get("/")
async def read_root() -> dict:
    """Root endpoint that returns a simple JSON greeting.

    Returns
    -------
    dict
        A dictionary with a welcome message.
    """
    return {"message": "Hello from FastAPI on IIS!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None) -> dict:
    """Return item information.

    Parameters
    ----------
    item_id : int
        The ID of the item requested.
    q : str | None, optional
        An optional query string parameter that can be used to filter or
        customise the response.  Defaults to ``None``.

    Returns
    -------
    dict
        A dictionary containing the item ID and the value of ``q`` (if
        provided).
    """
    return {"item_id": item_id, "q": q}

