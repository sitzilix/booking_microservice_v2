from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import Base

class Author(Base):
    __tablename__ = "authors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    
    books: Mapped[List["Book"]] = relationship(back_populates="author")
    
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"