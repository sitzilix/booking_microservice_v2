from pydantic import BaseModel, Field

class BookingBase(BaseModel):
    user_id: int = Field(..., gt=0)
    book_id: int = Field(..., gt=0)
    
    status: str = Field("pending", max_length=20)

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True

