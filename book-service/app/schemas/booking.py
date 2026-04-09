from datetime import datetime

from pydantic import BaseModel, Field

class BookingBase(BaseModel):
    user_id: int = Field(..., gt=0)
    book_id: int = Field(..., gt=0)
    
    status: str = Field("pending", max_length=20,
                        description="The status of the booking (e.g., pending, confirmed, cancelled)")

class BookingCreate(BookingBase):
    pass

class BookShort(BaseModel):
    id: int
    title: str
    price: int

class BookingResponse(BookingBase):
    id: int
    created_at: datetime 
    book: BookShort  # Вложенная схема
    
    class Config:
        from_attributes = True

