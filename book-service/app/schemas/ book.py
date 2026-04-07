from pydantic import BaseModel, Field
from typing import Optional
from .author import AuthorResponse
from .genre import GenreResponse

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,
                       description="The title of the book")
    
    description: Optional[str] = Field(None, max_length=1000,
                        description="The description of the book")
    
    price: float = Field(..., gt=0, 
                         description="The price of the book")

class BookCreate(BookBase):
    author_id : int = Field(..., gt=0, 
        description="The ID of the author")
    genre_id : int = Field(..., gt=0, 
        description="The ID of the genre")

class BookResponse(BookBase):
    id: int
    author: AuthorResponse
    genre: GenreResponse
    
    class Config:
        from_attributes = True
        
