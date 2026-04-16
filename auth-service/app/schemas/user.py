from pydantic import BaseModel, Field, EmailStr, ConfigDict

# Общие поля, которые есть везде
class UserBase(BaseModel):
    email: EmailStr

# Поля для регистрации (Email + Пароль)
class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8,   # Для пароля лучше минимум 8
        max_length=128, # Слишком длинный пароль (1000) bcrypt может не переварить
        description="Пароль пользователя"
    )

# Поля для ответа API (ID + Email)
class UserResponse(UserBase):
    id: int
    
    # Современный способ включить поддержку ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)