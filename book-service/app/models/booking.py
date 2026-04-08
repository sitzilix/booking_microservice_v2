from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    
    user_id: Mapped[int] = mapped_column(index=True)
    
    status: Mapped[str] = mapped_column(String(20), default="pending") # pending, confirmed, cancelled
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    book: Mapped["Book"] = relationship(back_populates="bookings")
    
    def __repr__(self):
        return f"<Booking(id={self.id}, book_id={self.book_id}, user_id={self.user_id})>"