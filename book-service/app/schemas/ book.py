from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    
class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    
    class Config:
        from_attributes = True
        
