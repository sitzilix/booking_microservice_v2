from pydantic import BaseModel, Field

class GenreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="The name of the genre")
    
class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int
    
    class Config:
        from_attributes = True