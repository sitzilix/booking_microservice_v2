from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str 
    
class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int
    
    class Config:
        from_attributes = True