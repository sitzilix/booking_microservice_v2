from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=128, 
        description="Регистрация пользователя"
    )

class UserToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserLogin(UserBase):
    password: str = Field(...,
                          description="Логин пользователя")
    
class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
