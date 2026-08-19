from pydantic import BaseModel
from typing import Optional


class NewFeed(BaseModel):
    name: str | None = None
    link: Optional[str] = None
