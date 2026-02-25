from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

class TokenResponse(BaseModel):
    access_token: str
    role: str