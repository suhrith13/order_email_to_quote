"""Validated schema for what the LLM must extract from a free-text order email."""

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str = Field(..., description="Product as described in the email, e.g. '1/2 inch copper elbow'")
    quantity: int = Field(..., ge=1, description="Quantity ordered")
    spec: str | None = Field(None, description="Size/spec/material detail if mentioned, else null")


class ExtractedOrder(BaseModel):
    items: list[LineItem]
    customer_note: str | None = Field(None, description="Any delivery/urgency note in the email, else null")
