from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import Base


class Genre(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    books: Mapped[List["Book"]] = relationship(back_populates="genre")
    
    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"