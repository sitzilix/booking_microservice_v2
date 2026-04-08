from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.dao.author_dao import AuthorDAO
from app.schemas.author import AuthorCreate, AuthorResponse

class AuthorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_authors(self) -> list[AuthorResponse]:
        authors = await AuthorDAO.get_all(self.db)
        return [AuthorResponse.model_validate(author) for author in authors]
        
    async def get_author_by_id(self, author_id: int) -> AuthorResponse:
        author = await AuthorDAO.get_by_id(self.db, author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Author with ID {author_id} not found"
            )
        return AuthorResponse.model_validate(author)
    
    async def create_author(self, author_data: AuthorCreate) -> AuthorResponse:
        new_author = await AuthorDAO.create(self.db, author_data)
        
        try:
            await self.db.commit()
            await self.db.refresh(new_author)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Failed to create author: {str(e)}"
            )
    
        return AuthorResponse.model_validate(new_author)