import uuid
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    previous_data: list[str] = Field(...)
    custom_icons: list[str] = Field(...)
    constant_icons: list[str] = Field(...)
    
class UserUpdate(BaseModel):
    previous_data: Optional[list[str]]
    custom_icons: Optional[list[str]]
    constant_icons: Optional[list[str]]