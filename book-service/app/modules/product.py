from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

class Genre(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    books: Mapped[List["Book"]] = relationship(back_populates="genre")
    
    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"
    
class Author(Base):
    __tablename__ = "authors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    
    books: Mapped[List["Book"]] = relationship(back_populates="author")
    
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"
    
class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    price: Mapped[int] = mapped_column(default=0)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
    genre: Mapped["Genre"] = relationship(back_populates="books")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"
    
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